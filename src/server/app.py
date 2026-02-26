import os
import requests
import jsonpickle
import httpx
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.routing import RedirectResponse
from pydantic import BaseModel

from fastapi import FastAPI, Request, Form, status
from fastapi import HTTPException

from src.server.database.databaseConnection import (
    loginUser, registerUser, initialize, getCurrentUser, signOutUser,
    getUserPlants, deleteUserPlant, changePassword, addUserPlant
)
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # src/server

# Starts the fastapi RESTful api
app = FastAPI()

# Loads the ..env file containing environment variables
load_dotenv()

# Mounts the app to a path, reason unclear
# app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
# Here we define where the templates are stored.
# We use templates because you can insert variables into
# the HTML, CSS, or Javascript of the file to make it easier
# to
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
# Starts the database client.
# NOTICE: Communication with the database client will have to be changed to at least
# NOTICE: partly frontend for this app to function as expected
#
# initialize()
# @app.on_event("startup")
def startup_event():
    initialize()

@app.get("/")
async def main(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        print("found user")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/home")
async def home(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("home.tpl", {"request": request, "email": current_user.user.email})

    # Redirects user to the home page,
    # status_code is 303 because that makes the redirect request a GET request
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    response.delete_cookie("access_token")

    return response
@app.get("/login")
async def login(request: Request):
    current_user = get_current_user_from_cookie(request)
    if current_user is not None:
        print("found user")
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        print("no user found")
        return templates.TemplateResponse("login.tpl", {"request": request})
@app.post("/login")
async def login(request: Request, email: str = Form(), password: str = Form()):
    print(email, password)
    session = loginUser(email, password)
    print(session)

    if session is not None:
        redirect = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
        
        redirect.set_cookie(
            key="access_token",
            value=session.access_token,
            httponly=True,
            samesite="lax"
        )

        return redirect
    else:
        return templates.TemplateResponse(
            "login.tpl",
            {"request": request, "errorCode": "invalid login"}
        )


@app.get("/register")
async def registerPage(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        print("found user")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    else:
        print("no user found")
        return templates.TemplateResponse("register.tpl", {"request": request})
@app.post("/register")
async def register(request: Request, email: str = Form(), password: str = Form()):
    print(email, password)
    response = registerUser(email, password)

    if response == "success":
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    else:
        print(response)
        return templates.TemplateResponse("register.tpl", {"request": request, "errorCode": response})

@app.get("/myPlants")
async def myPlants(request: Request):
    token = request.cookies.get("access_token")
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        user_id = current_user.user.id
        plants = getUserPlants(user_id, token)

        return templates.TemplateResponse("myPlants.tpl", {"request": request, "plants" : plants, "email": current_user.user.email})
    else:
        print("no user found")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

@app.delete("/myPlants/delete/{plant_id}")
async def myPlantDelete(request: Request, plant_id: int):
    token = request.cookies.get("access_token")
    current_user = get_current_user_from_cookie(request)
    user_id = current_user.user.id
    deleteUserPlant(plant_id, user_id, token)

@app.get("/account")
async def myAccount(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("account.tpl", {"request": request, "email" : current_user.user.email})
    else:
        print("no user found")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/allPlants")
async def allPlants(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        plants = await getAllSpecies()

        return templates.TemplateResponse("allPlants.tpl", {"request": request, "plants" : plants, "email": current_user.user.email})
    else:
        print("no user found")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/addPlant")
async def addPlant(
    request: Request,
    plant_id: int = Form(...),
    common_name: str = Form(...),
    last_watered: str = Form(None)   # optional, format: YYYY-MM-DD
):
    current_user = get_current_user_from_cookie(request)

    if current_user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user_id = current_user.user.id

    result = addUserPlant(
        user_id=user_id,
        plant_id=plant_id,
        common_name=common_name,
        last_watered=last_watered
    )

    # If insert failed, you can show an error page or return to allPlants with an error query param.
    if isinstance(result, str) and "error" in result.lower():
        return templates.TemplateResponse(
            "allPlants.tpl",
            {"request": request, "error": result, "email": current_user.user.email, "plants": await getAllSpecies()}
        )

    return RedirectResponse(url="/myPlants", status_code=status.HTTP_303_SEE_OTHER)

async def getAllSpecies():
    resp = await http_client.get("https://trefle.io/api/v1/plants", params={"token": os.getenv("API_KEY")})
    resp.raise_for_status()
    return jsonpickle.decode(resp.text)

def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        client = get_client_for_token(token)
        user = client.auth.get_user()
        return user
    except Exception:
        return None

async def searchForSpecies(searchTerm):
    resp = await http_client.get("https://trefle.io/api/v1/plants", params={"token": os.getenv("API_KEY"), "q": searchTerm})
    resp.raise_for_status()
    return jsonpickle.decode(resp.text)

# A class is created so that the /account/change_password endpoint can recognize the data sent to it
# by using this class as a "base model"
class PasswordChangeRequest(BaseModel):
    new_password: str

# This method translates the received JSON from the body of the request
# to an PasswordChangeRequest object with a new_password attribute
@app.post("/account/change_password")
def change_password(request : Request, password_request : PasswordChangeRequest):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    result = changePassword(token, password_request.new_password)

    if result != "success":
        raise HTTPException(status_code=400, detail=result)

    return {"message": "Password updated"}

class AddPlantRequest(BaseModel):
    plant_id: int
    common_name: str

@app.post("/myPlants/addPlant")
async def add_plant(request: Request, req: AddPlantRequest):
    token = request.cookies.get("access_token")
    current_user = get_current_user_from_cookie(request)
    if current_user is None:
        return {"ok": False, "error": "NOT_LOGGED_IN"}

    user_id = current_user.user.id
    result = addUserPlant(user_id, req.plant_id, req.common_name, token)

    # crude success check
    if isinstance(result, list):
        return {"ok": True, "data": result}

    return {"ok": False, "error": result}



