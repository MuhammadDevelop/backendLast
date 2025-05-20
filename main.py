from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import smtplib
import random
import hashlib
import shutil
import os
from email.mime.text import MIMEText

app = FastAPI()
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}
# Statik fayllar uchun papkalarni yaratish
os.makedirs("avatars", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# Statik fayllarni ulash
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email sozlamalari
SENDER_EMAIL = "muham20021202@gmail.com"
APP_PASSWORD = "kxnx qmzg qtbc guhm"
ADMIN_EMAIL = "muham20021202@gmail.com"

# ---- MODELLAR ----

class Lesson(BaseModel):
    id: int
    category: Dict[str, str]
    title: Dict[str, str]
    description: Dict[str, str]
    subtitle: Dict[str, str]
    answer: Dict[str, str]
    video_url: Optional[str] = None  # video_url endi majburiy emas


class RegisterInput(BaseModel):
    name: str
    email: str
    password: str

class VerifyInput(BaseModel):
    code: str

class Comment(BaseModel):
    name: Optional[str] = None
    email: str
    message: str

class UserOutput(BaseModel):
    email: str
    image: str
    name: Optional[str] = None

# ---- MA'LUMOTLAR OMBORI ----

lessons = [
    {
        "id": 1,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
            
        },
        "title": {
            "uz": "Word kirish va sozlamalar",
            "rus": "Введение в Word и настройки",
            "eng": "Introduction to Word and settings"
        },
        "description": {
            "uz": "Word dasturiga kirish va  sozlamalar",
            "rus": "Введение в программу Word и настройки",
            "eng": "Introduction to Word and settings"
        },
        "subtitle": {
            "uz": "Word Nima uchun kerak?",
            "rus": "Зачем нужен Word?",
            "eng": "Why is Word needed?"
        },
        "answer": {
            "uz": "Microsoft Word matn yaratish, tahrirlash va formatlash uchun kerak",
            "rus": "Microsoft Word нужен для создания, редактирования и форматирования текста",
            "eng": "Microsoft Word is used to create, edit, and format text"
        },
            "video_url":"https://backendlast-1.onrender.com/videos/darsWord-1.mp4"
       
    },
    {
        "id": 2,
         "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
            
        },
        "title": {
            "uz": "Fayl va Gavnaya bo'limi bilan ishlash",
            "rus": "Работа с файлами и главной страницей",
            "eng": "Working with files and the homepage"
        },
        "description": {
            "uz": "Vstavka bo'limi haqida.",
            "rus": "О разделе Вставка.",
            "eng": "About the Insert section."
        },
        "subtitle": {
            "uz": "Gavnaya bo'limi bizga nima uchun kerak?",
            "rus": "Зачем нам нужен раздел Вставка?",
            "eng": "Why do we need the Insert section?"
        },
        "answer": {
            "uz": "Gavnaya bo‘lim — bu har qanday sayt yoki dasturda asosiy sahifa (ya’ni boshlang‘ich joy). Bu bo‘lim foydalanuvchini dastur yoki sayt bilan tanishtiradi.",
            "rus": "Главный раздел — это главная страница любого сайта или программы (то есть начальная точка). Этот раздел знакомит пользователя с сайтом или программой.",
            "eng": "The main section is the homepage of any website or application (that is, the starting point). This section introduces the user to the website or application."
        },
         "video_url":"https://backendlast-1.onrender.com/videos/darsWord-2.mp4"
    },
    {
        "id": 3,
        "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
            
        },
        "title": {
            "uz": "Dizayn va Maket bo'limlari",
            "rus": "Разделы Дизайн и Макет",
            "eng": "Design and Layout sections"
        },
        "description": {
            "uz": "Dizayn va Maket bo'limlari haqida",
            "rus": "О разделах Дизайн и Макет",
            "eng": "About Design and Layout sections"
        },
        "subtitle": {
            "uz": "Dizayn va Maket bo'limida nimalar o'rganamiz?",
            "rus": "Что мы изучаем в разделах Дизайн и Макет?",
            "eng": "What do we learn in Design and Layout sections?"
        },
        "answer": {
            "uz": "Dizayn bo‘limida interfeys, shrift, tugmalar, sahifa ko‘rinishi, Maket bo‘limida esa joylashuv va o‘lchamlar sozlanadi",
            "rus": "В разделе Дизайн настраивается интерфейс, шрифты, кнопки, внешний вид страницы, а в Макете — расположение и размеры",
            "eng": "Design section configures interface, fonts, buttons, page look; Layout section manages positioning and sizing"
        },
        "video_url":"https://backendlast-1.onrender.com/videos/darsWord-3.mp4"
    },
    {
        "id": 4,
      "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
            
        },
        "title": {
            "uz": "Excelga kirish",
            "rus": "Введение в Excel",
            "eng": "Introduction to Excel"
        },
        "description": {
            "uz": "Excel dasturiga kirish.",
            "rus": "Введение в программу Excel.",
            "eng": "Getting started with Excel."
        },
        "subtitle": {
            "uz": "Excel nima uchun kerak?",
            "rus": "Зачем нужен Excel?",
            "eng": "Why is Excel needed?"
        },
        "answer": {
            "uz": "Excel maʼlumotlarni tartiblash, hisoblash va tahlil qilish uchun kerak.",
            "rus": "Excel нужен для сортировки, вычислений и анализа данных.",
            "eng": "Excel is used to organize, calculate, and analyze data."
        },
      "video_url":"https://backendlast-1.onrender.com/videos/darsWord-4.mp4"
    },
     {
        "id": 5,
       "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
            
        },
        "title": {
            "uz": "Excelga kirish",
            "rus": "Введение в Excel",
            "eng": "Introduction to Excel"
        },
        "description": {
            "uz": "Excel dasturiga kirish.",
            "rus": "Введение в программу Excel.",
            "eng": "Getting started with Excel."
        },
        "subtitle": {
            "uz": "Excel nima uchun kerak?",
            "rus": "Зачем нужен Excel?",
            "eng": "Why is Excel needed?"
        },
        "answer": {
            "uz": "Excel maʼlumotlarni tartiblash, hisoblash va tahlil qilish uchun kerak.",
            "rus": "Excel нужен для сортировки, вычислений и анализа данных.",
            "eng": "Excel is used to organize, calculate, and analyze data."
        },
      "video_url":"https://backendlast-1.onrender.com/videos/darsWord-5.mp4"
    },
     {
        "id": 6,
         "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
            
        },
        "title": {
            "uz": "Excelga kirish",
            "rus": "Введение в Excel",
            "eng": "Introduction to Excel"
        },
        "description": {
            "uz": "Excel dasturiga kirish.",
            "rus": "Введение в программу Excel.",
            "eng": "Getting started with Excel."
        },
        "subtitle": {
            "uz": "Excel nima uchun kerak?",
            "rus": "Зачем нужен Excel?",
            "eng": "Why is Excel needed?"
        },
        "answer": {
            "uz": "Excel maʼlumotlarni tartiblash, hisoblash va tahlil qilish uchun kerak.",
            "rus": "Excel нужен для сортировки, вычислений и анализа данных.",
            "eng": "Excel is used to organize, calculate, and analyze data."
        },
         "video_url":"https://backendlast-1.onrender.com/videos/darsWord-6.mp4"
    },
     {
        "id": 7,
       "category": {
            "uz": "Word darslari",
            "rus": "Уроки Word",
            "eng": "Word lessons"
            
        },
        "title": {
            "uz": "Excelga kirish",
            "rus": "Введение в Excel",
            "eng": "Introduction to Excel"
        },
        "description": {
            "uz": "Excel dasturiga kirish.",
            "rus": "Введение в программу Excel.",
            "eng": "Getting started with Excel."
        },
        "subtitle": {
            "uz": "Excel nima uchun kerak?",
            "rus": "Зачем нужен Excel?",
            "eng": "Why is Excel needed?"
        },
        "answer": {
            "uz": "Excel maʼlumotlarni tartiblash, hisoblash va tahlil qilish uchun kerak.",
            "rus": "Excel нужен для сортировки, вычислений и анализа данных.",
            "eng": "Excel is used to organize, calculate, and analyze data."
        },
      "video_url":"https://backendlast-1.onrender.com/videos/darsWord-7.mp4"
    }
      
]



TEMP_USERS: Dict[str, dict] = {}
USERS: List[Dict[str, str]] = []
comments: Dict[int, List[Comment]] = {}

# ---- API YO‘LLARI ----

@app.get("/lessons", response_model=List[Lesson])
def get_lessons(lang: Optional[str] = Query("uz")):
    result = []
    for lesson in lessons:
        result.append(Lesson(
            id=lesson["id"],
            category={lang: lesson["category"].get(lang, lesson["category"]["uz"])},
            title={lang: lesson["title"].get(lang, lesson["title"]["uz"])},
            description={lang: lesson["description"].get(lang, lesson["description"]["uz"])},
            subtitle={lang: lesson["subtitle"].get(lang, lesson["subtitle"]["uz"])},
            answer={lang: lesson["answer"].get(lang, lesson["answer"]["uz"])},
          
        ))
    return result

@app.get("/lessons/{lesson_id}", response_model=Lesson)
def get_lesson_by_id(lesson_id: int):
    for lesson in lessons:
        if lesson["id"] == lesson_id:
            return Lesson(**lesson)
    raise HTTPException(status_code=404, detail="Bunday IDdagi dars topilmadi")

@app.post("/register")
def register(user: RegisterInput):
    if user.email in TEMP_USERS:
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan.")
    verify_code = str(random.randint(100000, 999999))
    TEMP_USERS[user.email] = {
        "password": user.password,
        "code": verify_code,
        "name": user.name
    }
    msg = MIMEText(f"Sizning tasdiqlash kodingiz: {verify_code}")
    msg["Subject"] = "Tasdiqlash kodi"
    msg["From"] = SENDER_EMAIL
    msg["To"] = user.email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    return {"message": "Kod yuborildi"}

@app.post("/verify")
def verify_code(data: VerifyInput):
    for email, user_data in TEMP_USERS.items():
        if user_data["code"] == data.code:
            email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
            image_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"
            USERS.append({
                "email": email,
                "password": user_data["password"],
                "image": image_url,
                "name": user_data.get("name")
            })
            del TEMP_USERS[email]
            return {"message": "Tasdiqlandi va ro'yxatdan o'tdingiz", "image": image_url}
    raise HTTPException(status_code=400, detail="Kod noto‘g‘ri")

@app.post("/upload-avatar")
async def upload_avatar(email: str = Form(...), image: UploadFile = File(...)):
    filename = f"avatars/{email.replace('@', '_')}.png"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    file_url = f"https://backendthree-sc1q.onrender.com/avatars/{email.replace('@', '_')}.png"
    return {"message": "Rasm saqlandi", "image": file_url}

@app.post("/lessons/{lesson_id}/comments")
def add_comment(lesson_id: int, comment: Comment):
    lesson_ids = [lesson["id"] for lesson in lessons]
    if lesson_id not in lesson_ids:
        raise HTTPException(status_code=404, detail="Bunday IDdagi dars topilmadi")

    if lesson_id not in comments:
        comments[lesson_id] = []
    comments[lesson_id].append(comment)

    comment_name = comment.name or "Ism ko'rsatilmagan"

    # Admin email
    admin_body = f"""🔔 Yangi izoh keldi!

🆔 Dars ID: {lesson_id}
👤 Ism: {comment_name}
📧 Email: {comment.email}

💬 Xabar:
{comment.message}
"""
    admin_msg = MIMEText(admin_body)
    admin_msg["Subject"] = f"Dars {lesson_id} uchun yangi izoh"
    admin_msg["From"] = SENDER_EMAIL
    admin_msg["To"] = ADMIN_EMAIL
    admin_msg["Reply-To"] = comment.email

    # User email
    user_body = f"""Salom {comment_name},

Izohingiz uchun rahmat! Tez orada sizga javob beramiz.

Hurmat bilan,  
Bilim ol jamoasi
"""
    user_msg = MIMEText(user_body)
    user_msg["Subject"] = "Izohingiz qabul qilindi"
    user_msg["From"] = SENDER_EMAIL
    user_msg["To"] = comment.email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(admin_msg)
        server.send_message(user_msg)

    return {"message": "Izoh saqlandi va email yuborildi"}

@app.get("/users", response_model=List[UserOutput])
def get_users():
    return USERS
