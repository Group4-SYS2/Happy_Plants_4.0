from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapi import FastAPI, Request, Form

from database.databaseConnection import loginUser, registerUser

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

from fastapi.responses import RedirectResponse

@app.get("/login")
async def home(request: Request):
    return templates.TemplateResponse("login.tpl", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(), password: str = Form()):
    print(email, password)
    result = loginUser(email, password)
    print(result)

    if result["status"] == "success":
        return templates.TemplateResponse("main.tpl", {"request": request, "email": email})

@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.tpl", {"request": request})

@app.post("/register")
async def login(request: Request, email: str = Form(), password: str = Form()):
    print(email, password)
    result = registerUser(email, password)

    if result["status"] == "success":
        return templates.TemplateResponse("login.tpl", {"request": request})
    else:
        print(result["message"])
        return templates.TemplateResponse("register.tpl", {"request": request})


