from fastapi import APIRouter, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.server.database.databaseConnection import loginUser, registerUser
from utils.auth import get_current_user_from_cookie

router = APIRouter()
templates = Jinja2Templates(directory="src/server/templates")

@router.get("/")
async def main(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        print("found user")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/home")
async def home(request: Request):
    current_user = get_current_user_from_cookie(request)
    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("home.tpl", {"request": request, "email": current_user.user.email})

    # Redirects user to the home page,
    # status_code is 303 because that makes the redirect request a GET request
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/login")
async def login_page(request: Request):
    current_user = get_current_user_from_cookie(request)
    if current_user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.tpl", {"request": request})


@router.post("/login")
async def login(request: Request, email: str = Form(), password: str = Form()):
    session = loginUser(email, password)

    if session:
        response = RedirectResponse("/home", status_code=303)
        response.set_cookie("access_token", session.access_token, httponly=True)
        return response

    return templates.TemplateResponse("login.tpl", {"request": request, "errorCode": "invalid login"})


@router.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response


@router.get("/account")
async def myAccount(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("account.tpl", {"request": request, "email" : current_user.user.email})
    else:
        print("no user found")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)