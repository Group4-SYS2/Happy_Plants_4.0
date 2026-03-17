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
    loginUser, registerUser, initialize, signOutUser,
    getUserPlants, deleteUserPlantByRowId, changePassword, addUserPlant, get_client_for_token, markPlantWatered
)
from datetime import date, datetime
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
http_client = httpx.AsyncClient()
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
   # print(session)

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

    if current_user is None:
        return RedirectResponse(url="/home", status_code=303)

    user_id = current_user.user.id
    plants = getUserPlants(user_id, token)

    for plant in plants:
        try:
            species = await getSpeciesById(plant["plant_id"])
            data = species.get("data", {})
            growth = data.get("growth") or {}

            humidity = (
                growth.get("soil_humidity")
                or growth.get("atmospheric_humidity")
            )

        except Exception:
            humidity = None

        plant["watering_status"] = build_watering_status(
            plant.get("last_watered"),
            humidity,
        )

    return templates.TemplateResponse(
        "myPlants.tpl",
        {"request": request, "plants": plants, "email": current_user.user.email},
    )
@app.delete("/myPlants/delete/{row_id}")
async def myPlantDelete(request: Request, row_id: int):
    token = request.cookies.get("access_token")
    current_user = get_current_user_from_cookie(request)

    if current_user is None or token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = current_user.user.id

    deleted_rows, err = deleteUserPlantByRowId(row_id=row_id, user_id=user_id, token=token)

    if err:
        raise HTTPException(status_code=500, detail=err)

    if not deleted_rows:
        raise HTTPException(status_code=404, detail="No row deleted (wrong row_id or blocked by RLS).")

    return {"ok": True, "deleted": len(deleted_rows)}

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

    if current_user is None:
        return RedirectResponse(url="/home", status_code=303)

    plants = await getAllSpecies()

    for plant in plants.get("data", []):
        print("DEBUG keys:", plant.keys())
        print("DEBUG growth:", plant.get("growth"))
        break

 
    for plant in plants.get("data", [])[:20]:  # begränsa till 20 för hastighet
        try:
            species_detail = await getSpeciesById(plant["id"])
            data = species_detail.get("data", {})
            growth = data.get("growth") or {}

            light_value = growth.get("light")
            water_value = growth.get("soil_humidity") or growth.get("atmospheric_humidity")

        except Exception:
            light_value = None
            water_value = None

        plant["light_text"] = scale_to_text(light_value)
        plant["water_text"] = scale_to_text(water_value)

    return templates.TemplateResponse(
        "allPlants.tpl",
        {
            "request": request,
            "plants": plants,
            "email": current_user.user.email,
        },
    )

# @app.post("/addPlant")
# async def addPlant(
#     request: Request,
#     plant_id: int = Form(...),
#     common_name: str = Form(...),
#     last_watered: str = Form(None)   # optional, format: YYYY-MM-DD
# ):
#     current_user = get_current_user_from_cookie(request)
#
#     if current_user is None:
#         return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
#
#     user_id = current_user.user.id
#
#     result = addUserPlant(
#         user_id=user_id,
#         plant_id=plant_id,
#         common_name=common_name,
#         last_watered=last_watered
#     )
#
#     # If insert failed, you can show an error page or return to allPlants with an error query param.
#     if isinstance(result, str) and "error" in result.lower():
#         return templates.TemplateResponse(
#             "allPlants.tpl",
#             {"request": request, "error": result, "email": current_user.user.email, "plants": await getAllSpecies()}
#         )
#
#     return RedirectResponse(url="/myPlants", status_code=status.HTTP_303_SEE_OTHER)

async def getAllSpecies():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://trefle.io/api/v1/plants",
            params={"token": os.getenv("API_KEY")},
            timeout=20.0
        )
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
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://trefle.io/api/v1/plants",
            params={"token": os.getenv("API_KEY"), "q": searchTerm},
            timeout=20.0
        )
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



def scale_to_text(value):
    if value is None:
        return "Unknown"
    try:
        value = int(value)
    except (TypeError, ValueError):
        return "Unknown"

    if value <= 3:
        return "Low"
    if value <= 7:
        return "Medium"
    return "High"

async def getSpeciesById(species_id: int):
    resp = await http_client.get(
        f"https://trefle.io/api/v1/species/{species_id}",
        params={"token": os.getenv("API_KEY")}
    )
    resp.raise_for_status()
    return jsonpickle.decode(resp.text)

@app.get("/plant/{species_id}")
async def plant_info(request: Request, species_id: int):
    current_user = get_current_user_from_cookie(request)

    if current_user is None:
        return RedirectResponse(url="/login", status_code=303)

    species = await getSpeciesById(species_id)

    data = species.get("data", {})
    growth = data.get("growth") or {}

    light_value = growth.get("light")
    water_value = (
        growth.get("soil_humidity")
        or growth.get("atmospheric_humidity")
    )

    plant_info = {
        "common_name": data.get("common_name"),
        "scientific_name": data.get("scientific_name"),
        "family": data.get("family"),
        "light_text": scale_to_text(light_value),
        "water_text": scale_to_text(water_value),
    }

    return templates.TemplateResponse(
        "plantInfo.tpl",
        {
            "request": request,
            "plant": plant_info,
            "email": current_user.user.email,
        },
    )


def humidity_to_days(value: int | None) -> int:
    """Konverterar Trefle humidity → dagar mellan vattning"""
    if value is None:
        return 7

    try:
        value = int(value)
    except:
        return 7

    if value <= 3:
        return 14  # låg vattenbehov
    if value <= 6:
        return 7   # medium
    return 3       # hög vattenbehov

def build_watering_status(last_watered: str, humidity_value: int | None):
    interval_days = humidity_to_days(humidity_value)

    if not last_watered:
        return {"percent": 100, "needs_water": True}

    try:
        last_date = datetime.strptime(last_watered, "%Y-%m-%d").date()
    except Exception:
        return {"percent": 100, "needs_water": True}

    days_since = (date.today() - last_date).days
    percent = min(int((days_since / interval_days) * 100), 100)

    return {
        "percent": percent,
        "needs_water": days_since >= interval_days,
        "days_since": days_since,
        "interval_days": interval_days,
    }

@app.post("/myPlants/water/{row_id}")
async def water_plant(request: Request, row_id: int):
    print(" WATER ENDPOINT HIT", row_id)

    token = request.cookies.get("access_token")
    current_user = get_current_user_from_cookie(request)

    if current_user is None:
        print(" no user")
        raise HTTPException(status_code=401)

    user_id = current_user.user.id
    print("user:", user_id)

    result = markPlantWatered(user_id, row_id, token)

    print("DB result:", result)

    return RedirectResponse(url="/myPlants", status_code=303)