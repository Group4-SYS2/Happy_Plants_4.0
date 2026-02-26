import os
import requests
import jsonpickle
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.routing import RedirectResponse
from pydantic import BaseModel

from fastapi import FastAPI, Request, Form, status

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
# initialize()
@app.on_event("startup")
def startup_event():
    initialize()

# This is the FastAPI endpoint for the root of the app.
@app.get("/")
# This function gets triggered when a user visits the endpoint above.
async def main(request: Request):

    # Fetch the current user.
    current_user = getCurrentUser()

    # If the user is logged in, they get redirected to /home
    if current_user is not None:
        print("found user")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

    # If not, they go to /login
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

# This is the FastAPI endpoint for the home page of the app.
@app.get("/home")
async def home(request: Request):

    # Fetch the current user.
    current_user = getCurrentUser()

    # If user is logged in we give them the home.tpl file via Jinja2Templates.
    # We must always return the "request" parameter when we send a template.
    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("home.tpl", {"request": request, "email": current_user.user.email})
        # We insert the users email in an "email" variable.

    # Redirects user to the home page if they're not logged in.
    # we set status_code to 303 because that makes the redirect request a GET request,
    # which is required for our endpoint.
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout(request: Request):

    # Fetch the current user.
    current_user = getCurrentUser()

    # If there is a user logged in, they get signed out and then redirected to the "/" endpoint
    if current_user is not None:
        signOutUser()

    # Otherwise, they just get redirected instead.
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# Returns the login page if the user is not logged in already.
# As you can see, we reference "/login" twice.
# This is because one of the endpoints is for GET requests,
# and the other is for POST requests.
@app.get("/login") # Notice "app.get"
async def login(request: Request):
    current_user = getCurrentUser()
    if current_user is not None:
        print("found user")
        # If the user is logged in they go to the root of the app.
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        print("no user found")
        # Returns the login.tpl file.
        return templates.TemplateResponse("login.tpl", {"request": request})

# This endpoint receives the email and password from an HTML forms request.
# This is why the datatype of email and password is "Form()".
@app.post("/login") # Notice "app.post"
async def login(request: Request, email: str = Form(), password: str = Form()):
    print(email, password)
    response = loginUser(email, password)
    print(response)

    if response == "success":
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse("login.tpl", {"request": request, "errorCode": response})

@app.get("/register")
async def registerPage(request: Request):
    current_user = getCurrentUser()

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
    current_user = getCurrentUser()

    if current_user is not None:
        user_id = current_user.user.id
        plants = getUserPlants(user_id)

        return templates.TemplateResponse("myPlants.tpl", {"request": request, "plants" : plants, "email": current_user.user.email})
    else:
        print("no user found")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

@app.delete("/myPlants/delete/{plant_id}")
async def myPlantDelete(request: Request, plant_id: int):
    current_user = getCurrentUser()

    if current_user is None:
        return {"ok": False, "error": "NOT_LOGGED_IN"}

    user_id = current_user.user.id
    result = deleteUserPlant(plant_id, user_id)

    return {"ok": True}

@app.get("/account")
async def myAccount(request: Request):
    current_user = getCurrentUser()

    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("account.tpl", {"request": request, "email" : current_user.user.email})
    else:
        print("no user found")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/allPlants")
async def myPlants(request: Request):
    current_user = getCurrentUser()

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
    current_user = getCurrentUser()

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
    plantRequest = requests.get("https://trefle.io/api/v1/plants?token=" + os.getenv("API_KEY"))
    return jsonpickle.decode(plantRequest.text)

async def searchForSpecies(searchTerm):
    plantRequest = await requests.get("https://trefle.io/api/v1/plants?token=" + os.getenv("API_KEY") + "&q=" + searchTerm)
    return jsonpickle.decode(plantRequest.text)

# A class is created so that the /account/change_password endpoint can recognize the data sent to it
# by using this class as a "base model"
class PasswordChangeRequest(BaseModel):
    new_password: str

# This method translates the received JSON from the body of the request
# to a PasswordChangeRequest object with a new_password attribute
@app.post("/account/change_password")
def change_password(request : Request, password_request : PasswordChangeRequest):
    changePassword(password_request.new_password)


class AddPlantRequest(BaseModel):
    plant_id: int
    common_name: str

@app.post("/myPlants/addPlant")
async def add_plant(req: AddPlantRequest):
    current_user = getCurrentUser()
    if current_user is None:
        return {"ok": False, "error": "NOT_LOGGED_IN"}

    user_id = current_user.user.id
    result = addUserPlant(user_id, req.plant_id, req.common_name)

    # crude success check
    if isinstance(result, list):
        return {"ok": True, "data": result}

    return {"ok": False, "error": result}



