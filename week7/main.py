from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from mysql.connector import Error
import os
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="0okm9ijn")

# 靜態檔案和模板設定
static_path = os.path.join(os.path.dirname(__file__), "static")
templates_path = os.path.join(os.path.dirname(__file__), "templates")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    print(f"警告: static 資料夾不存在於 {static_path}")

templates = Jinja2Templates(directory="templates")

# 資料庫連接函式
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="website"
        )
        print("資料庫連接成功")
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

# 會員頁面
@app.get("/member", response_class=HTMLResponse)
async def member_page(request: Request):
    # 檢查登入狀態
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        return RedirectResponse(url="/", status_code=303)
    
    # 取得會員資訊
    member_id = request.session.get("member_id", "")
    member_name = request.session.get("member_name", "")
    member_email = request.session.get("member_email", "")
    
    print(f"會員頁面載入: {member_name} (ID: {member_id})")
    
    # 渲染success.html
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "member_id": member_id,  
            "member_name": member_name,
            "member_email": member_email
        }
    )

class NameUpdateRequest(BaseModel):
    name: str

# 更新姓名API
@app.patch("/api/member")
async def update_member_name(request: Request, name_data: NameUpdateRequest):
    
    # 檢查是否已登入
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        print("未登入用戶嘗試更新姓名")
        return {"error": True}
    
    # 取得當前登入會員的ID
    member_id = request.session.get("member_id")
    new_name = name_data.name.strip()
    
    # 驗證姓名不為空
    if not new_name:
        print("姓名不能為空")
        return {"error": True}
    
    # 連接資料庫
    con = get_db_connection()
    if not con:
        print("資料庫連接失敗")
        return {"error": True}
    
    try:
        cursor = con.cursor()
        # 更新姓名
        cursor.execute(
            "UPDATE member SET name = %s WHERE id = %s",
            (new_name, member_id)
        )
        con.commit()
        
        # 檢查是否有更新任何記錄
        if cursor.rowcount > 0:
            # 更新 Session 中的姓名
            request.session["member_name"] = new_name
            print(f"更新成功: 會員 ID {member_id} 的姓名更新為 {new_name}")
            return {"ok": True}
        else:
            print(f"更新失敗: 找不到會員 ID {member_id}")
            return {"error": True}
            
    except Error as e:
        print(f"更新姓名錯誤: {e}")
        return {"error": True}
    finally:
        cursor.close()
        con.close()

# 查詢紀錄API
@app.get("/api/member/querylogs")
async def get_member_querylogs(request: Request):
    
    # 檢查是否已登入
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        print("未登入用戶嘗試查詢紀錄")
        return {"data": None}
    
    # 取得當前登入會員的ID
    queried_id = request.session.get("member_id")
    
    # 連接資料庫
    con = get_db_connection()
    if not con:
        print("資料庫連接失敗")
        return {"data": None}
    
    try:
        cursor = con.cursor(dictionary=True)
        
        # 查詢最近10筆查詢紀錄(自己查詢自己的記錄)
        cursor.execute("""
            SELECT member.name, querylogs.time
            FROM querylogs
            JOIN member ON querylogs.querier_id = member.id
            WHERE querylogs.queried_id = %s
            ORDER BY querylogs.time DESC
            LIMIT 10
        """, (queried_id,))
        
        logs = cursor.fetchall()
        
        if logs:
            # 格式化時間為YYYY-MM-DD HH:MM:SS
            formatted_logs = []
            for log in logs:
                formatted_logs.append({
                    "name": log["name"],
                    "time": log["time"].strftime("%Y-%m-%d %H:%M:%S")
                })
            
            print(f"查詢紀錄成功: 找到 {len(formatted_logs)} 筆記錄")
            return {"data": formatted_logs}
        else:
            print(f"查詢紀錄: 無記錄")
            return {"data": []}
            
    except Error as e:
        print(f"查詢紀錄錯誤: {e}")
        return {"data": None}
    finally:
        cursor.close()
        con.close()

# 會員查詢API
@app.get("/api/member/{member_id}")
async def get_member_api(request: Request, member_id: int):
    
    # 檢查是否已登入
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        print(f"未登入用戶嘗試查詢會員 {member_id}")
        return {"data": None}
    
    # 取得當前登入會員的ID
    querier_id = request.session.get("member_id")
    
    # 連接資料庫
    con = get_db_connection()
    if not con:
        print("資料庫連接失敗")
        return {"data": None}
    
    try:
        cursor = con.cursor(dictionary=True)
        
        # 查詢會員資料
        cursor.execute("SELECT id, name, email FROM member WHERE id = %s", (member_id,))
        member = cursor.fetchone()
        
        if member:
            # 記錄查詢紀錄
            if querier_id != member_id:
                cursor.execute(
                    "INSERT INTO querylogs (queried_id, querier_id) VALUES (%s, %s)",
                    (member_id, querier_id)
                )
                con.commit()
                print(f"查詢紀錄已記錄: 會員 {querier_id} 查詢了會員 {member_id}")
            
            print(f"查詢成功: {member['name']} (ID: {member_id})")
            return {
                "data": {
                    "id": member["id"],
                    "name": member["name"],
                    "email": member["email"]
                }
            }
        else:
            print(f"查無會員 ID: {member_id}")
            return {"data": None}
            
    except Error as e:
        print(f"查詢會員錯誤: {e}")
        return {"data": None}
    finally:
        cursor.close()
        con.close()

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
        # 檢查電子郵件是否已存在
        cursor.execute("SELECT email FROM member WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)

        # 新增會員
        cursor.execute(
            "INSERT INTO member(name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        con.commit()
        print(f"註冊成功: {name} ({email})")
        return RedirectResponse(url="/", status_code=303)

    except Error as e:
        print(f"註冊錯誤: {e}")
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
            # 設定Session
            request.session["LOGGED-IN"] = True
            request.session["member_id"] = member["id"]
            request.session["member_name"] = member["name"]
            request.session["member_email"] = member["email"]
            print(f"登入成功: {member['name']} (ID: {member['id']})")
            return RedirectResponse(url="/member", status_code=303)
        else:
            print(f"登入失敗: {email}")
            return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)

    except Error as e:
        print(f"登入錯誤: {e}")
        return RedirectResponse(url="/ohoh?msg=登入失敗，請稍後再試", status_code=303)
    finally:
        cursor.close()
        con.close()

@app.get("/logout")
async def logout(request: Request):
    member_name = request.session.get("member_name", "Unknown")
    request.session.clear()
    print(f"登出成功: {member_name}")
    return RedirectResponse(url="/", status_code=303)