import os
import requests
import jsonpickle
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.routing import RedirectResponse
from pydantic import BaseModel

from fastapi import FastAPI, Request, Form, status
from fastapi import HTTPException

from database.databaseConnection import supabaseClient
from database.databaseConnection import loginUser, registerUser, initialize, signOutUser, \
    getUserPlants, deleteUserPlant, changePassword, get_client_for_token

# Starts the fastapi RESTful api
app = FastAPI()

# Loads the .env file containing environment variables
load_dotenv()

# Mounts the app to a path, reason unclear
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define where the templates are stored
templates = Jinja2Templates(directory="templates")

# Starts the database client
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
async def myPlants(request: Request):
    current_user = get_current_user_from_cookie(request)

    if current_user is not None:
        plants = await getAllSpecies()

        return templates.TemplateResponse("allPlants.tpl", {"request": request, "plants" : plants, "email": current_user.user.email})
    else:
        print("no user found")
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/addPlant")
async def addPlant(request: Request):
    current_user = get_current_user_from_cookie(request)
    #Kommer behöva hämta och validera token här också sen när denna får kod


async def getAllSpecies():
    plantRequest = requests.get("https://trefle.io/api/v1/plants?token=" + os.getenv("API_KEY"))
    return jsonpickle.decode(plantRequest.text)

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
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    result = changePassword(token, password_request.new_password)

    if result != "success":
        raise HTTPException(status_code=400, detail=result)

    return {"message": "Password updated"}





