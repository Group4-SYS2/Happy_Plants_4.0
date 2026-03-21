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

@router.get("/myPlants")
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
@router.delete("/myPlants/delete/{row_id}")
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


@router.get("/allPlants")
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


async def getAllSpecies():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://trefle.io/api/v1/plants",
            params={"token": os.getenv("API_KEY")},
            timeout=20.0
        )
    resp.raise_for_status()
    return jsonpickle.decode(resp.text)