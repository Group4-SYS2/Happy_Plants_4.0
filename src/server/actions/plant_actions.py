from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.server.database.databaseConnection import (
    getUserPlants,
    deleteUserPlantByRowId,
)

from utils.auth import get_current_user_from_cookie
from services.trefle_api import get_all_species, get_species_by_id
from services.plant_service import build_watering_status, scale_to_text

router = APIRouter()

templates = Jinja2Templates(directory="src/server/templates")

from datetime import date, datetime

def scale_to_text(value):
    if value is None:
        return "Unknown"
    try:
        value = int(value)
    except:
        return "Unknown"

    if value <= 3:
        return "Low"
    if value <= 7:
        return "Medium"
    return "High"

@router.get("/plant/{species_id}")
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

@router.post("/myPlants/water/{row_id}")
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

@router.post("/myPlants/rename/{row_id}")
async def rename_plant(request: Request, row_id: int, req: RenamePlantRequest):

    token = request.cookies.get("access_token")
    current_user = get_current_user_from_cookie(request)

    if current_user is None or token is None:
        return {"ok": False, "error": "NOT_LOGGED_IN"}

    new_name = req.new_name.strip()

    if not new_name:
        return {"ok": False, "error": "Name cannot be empty"}

    user_id = current_user.user.id

    result = renameUserPlant(user_id, row_id, new_name, token)

    if isinstance(result, str):
        return {"ok": False, "error": result}

    return {"ok": True}