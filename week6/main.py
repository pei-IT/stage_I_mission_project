from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from mysql.connector import Error

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="0okm9ijn")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="website"
        )
        return connection
    except Error as e:
        print(f"資料庫連接錯誤: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        return RedirectResponse(url="/", status_code=303)

    # 取得會員資訊
    member_id = request.session.get("member_id", "")
    member_name = request.session.get("member_name", "")
    member_email = request.session.get("member_email", "")

    messages = []
    con = get_db_connection()
    if con:
        try:
            cursor = con.cursor(dictionary=True)
            # 查詢 message.member_id，讓前端能判斷是否顯示 X
            cursor.execute("""
                SELECT message.id,
                       message.member_id,
                       message.content,
                       message.time,
                       member.name
                FROM message
                JOIN member ON message.member_id = member.id
                ORDER BY message.time DESC
            """)
            messages = cursor.fetchall()
        except Error as e:
            print(f"查詢留言錯誤: {e}")
        finally:
            cursor.close()
            con.close()

    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "member_id": member_id,  
            "member_name": member_name,
            "member_email": member_email,
            "messages": messages
        }
    )

@app.get("/ohoh", response_class=HTMLResponse)
async def error_page(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"msg": msg}
    )

@app.post("/signup")
async def signup(
    request: Request, 
    name: str = Form(""), 
    email: str = Form(""), 
    password: str = Form("")
):   

    con = get_db_connection()
    if not con:
        return RedirectResponse(url="/ohoh?msg=資料庫連接失敗", status_code=303)

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT email FROM member WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)

        cursor.execute(
            "INSERT INTO member(name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        con.commit()
        return RedirectResponse(url="/", status_code=303)

    except Error as e:
        print(f"資料庫錯誤: {e}")
        return RedirectResponse(url="/ohoh?msg=註冊失敗，請稍後再試", status_code=303)
    finally:
        cursor.close()
        con.close()

@app.post("/login")
async def login(
    request: Request, 
    email: str = Form(""), 
    password: str = Form("")
):    

    con = get_db_connection()
    if not con:
        return RedirectResponse(url="/ohoh?msg=資料庫連接失敗", status_code=303)

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, email FROM member WHERE email = %s AND password = %s",
            (email, password)
        )
        member = cursor.fetchone()
        if member:
            request.session["LOGGED-IN"] = True
            request.session["member_id"] = member["id"]
            request.session["member_name"] = member["name"]
            request.session["member_email"] = member["email"]
            return RedirectResponse(url="/member", status_code=303)
        else:
            return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)

    except Error as e:
        print(f"資料庫錯誤: {e}")
        return RedirectResponse(url="/ohoh?msg=登入失敗，請稍後再試", status_code=303)
    finally:
        cursor.close()
        con.close()

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.post("/createMessage")
async def create_message(
    request: Request,
    content: str = Form("")
):
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        return RedirectResponse(url="/", status_code=303)

    member_id = request.session.get("member_id")
    content = content.strip()
    if not content:
        return RedirectResponse(url="/member", status_code=303)

    con = get_db_connection()
    if not con:
        return RedirectResponse(url="/member", status_code=303)

    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO message(member_id, content) VALUES (%s, %s)",
            (member_id, content)
        )
        con.commit()
    except Error as e:
        print(f"新增留言錯誤: {e}")
    finally:
        cursor.close()
        con.close()

    return RedirectResponse(url="/member", status_code=303)

@app.post("/deleteMessage")
async def delete_message(
    request: Request,
    message_id: int = Form(...)
):
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        return RedirectResponse(url="/", status_code=303)

    member_id = request.session.get("member_id")

    con = get_db_connection()
    if con:
        try:
            cursor = con.cursor()
            # 只能刪除自己的留言
            cursor.execute(
                "DELETE FROM message WHERE id = %s AND member_id = %s",
                (message_id, member_id)
            )
            con.commit()
        except Error as e:
            print(f"刪除留言錯誤: {e}")
        finally:
            cursor.close()
            con.close()

    return RedirectResponse(url="/member", status_code=303)
