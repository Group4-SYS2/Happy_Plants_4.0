import os
import requests
import jsonpickle
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.routing import RedirectResponse
from pydantic import BaseModel

from fastapi import FastAPI, Request, Form, status

from database.databaseConnection import loginUser, registerUser, getAllUsers, initialize, getCurrentUser, signOutUser, \
    getUserPlants, deleteUserPlant, changePassword

# Starts the fastapi RESTful api
app = FastAPI()

load_dotenv()

# Mounts the app to a path, reason unclear
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define where the templates are stored
templates = Jinja2Templates(directory="templates")

# Starts the database client
initialize()

@app.get("/")
async def main(request: Request):
    current_user = getCurrentUser()

    if current_user is not None:
        print("found user")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/home")
async def home(request: Request):
    current_user = getCurrentUser()

    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("home.tpl", {"request": request, "email": current_user.user.email})

    # Redirects user to the home page,
    # status_code is 303 because that makes the redirect request a GET request
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
@app.get("/logout")
async def logout(request: Request):
    current_user = getCurrentUser()

    if current_user is not None:
        signOutUser()

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
@app.get("/login")
async def login(request: Request):
    current_user = getCurrentUser()
    if current_user is not None:
        print("found user")
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        print("no user found")
        return templates.TemplateResponse("login.tpl", {"request": request})
@app.post("/login")
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
    user_id = current_user.user.id
    deleteUserPlant(plant_id, user_id)

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
# to an PasswordChangeRequest object with a new_password attribute
@app.post("/account/change_password")
def change_password(request : Request, password_request : PasswordChangeRequest):
    changePassword(password_request.new_password)






