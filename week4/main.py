from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import httpx

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="1qaz2wsx")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

HOTEL_API_URL_CH = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
HOTEL_API_URL_EN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

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
    return templates.TemplateResponse(
        request=request,
        name="success.html"
    )

@app.get("/ohoh", response_class=HTMLResponse)
async def error_page(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"msg": msg}
    )

#登入驗證端點
@app.post("/login")
async def login(request: Request, email: str = Form(""), password: str = Form("")):
    # 去除前後空白
    email = email.strip()
    password = password.strip()       
    # 檢查是否為空
    if not email or not password:        
        return RedirectResponse(
            url="/ohoh?msg=請輸入信箱和密碼",
            status_code=303
        )    
    # 驗證帳號密碼
    if email == "abc@abc.com" and password == "abc":        
        request.session["LOGGED-IN"] = True
        return RedirectResponse(
            url="/member",
            status_code=303
        )
    else:        
        return RedirectResponse(
            url="/ohoh?msg=信箱或密碼輸入錯誤",
            status_code=303
        )

@app.get("/logout")
async def logout(request: Request):
    request.session["LOGGED-IN"] = False
    return RedirectResponse(url="/", status_code=303)

# 旅館資訊頁面
@app.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def hotel_page(request: Request, hotel_id: int):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 獲取旅館中英文資料
            response_ch = await client.get(HOTEL_API_URL_CH)
            response_en = await client.get(HOTEL_API_URL_EN)            
            data_ch = response_ch.json()
            data_en = response_en.json()            
            # 從dict中取得list
            hotels_ch = data_ch.get("list", [])
            hotels_en = data_en.get("list", [])                
            # 尋找對應的旅館
            hotel_ch = None
            hotel_en = None            
            for h in hotels_ch:
                h_id = h.get("_id")
                try:
                    if int(h_id) == hotel_id:
                        hotel_ch = h                        
                        break
                except (ValueError, TypeError) as e:
                    print(f"ID 轉換失敗: {h_id}, 錯誤: {e}")
                    continue
            
            for h in hotels_en:
                h_id = h.get("_id")
                try:
                    if int(h_id) == hotel_id:
                        hotel_en = h                        
                        break
                except (ValueError, TypeError):
                    continue
            
            # 合併旅館中英文資料
            hotel = None
            if hotel_ch:
                hotel = {
                    "name_ch": hotel_ch.get("旅宿名稱", ""),
                    "name_en": hotel_en.get("hotel name", "") if hotel_en else "",
                    "phone": hotel_ch.get("電話或手機號碼", ""),
                    "address": hotel_ch.get("地址", ""),
                    "category": hotel_ch.get("旅館類別", "")
                }                        
            return templates.TemplateResponse(
                request=request,
                name="hotel.html",
                context={"hotel": hotel}
            )
            
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"錯誤: {e}")
        print(error_trace)
        return templates.TemplateResponse(
            request=request,
            name="hotel.html",
            context={"hotel": None}
        )

