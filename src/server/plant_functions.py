import os
import jsonpickle
import httpx
from fastapi import Request
from datetime import date, datetime

from src.server.database.databaseConnection import get_client_for_token

http_client = httpx.AsyncClient()

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

async def getSpeciesById(species_id: int):
    resp = await http_client.get(
        f"https://trefle.io/api/v1/species/{species_id}",
        params={"token": os.getenv("API_KEY")}
    )
    resp.raise_for_status()
    return jsonpickle.decode(resp.text)

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

def sort_plants(plants, sort_by):
    if not sort_by:
        return plants

    if sort_by == "nickname":
        # A → Z
        return sorted(
            plants,
            key=lambda p: (p.get("common_name") or "").lower()
        )

    if sort_by == "species":
        # Z → A
        return sorted(
            plants,
            key=lambda p: (p.get("scientific_name") or "").lower(),
        )

    if sort_by == "last_watered":
        # newest first
        return sorted(
            plants,
            key=lambda p: parse_date(p.get("last_watered")),
            reverse=True
        )


    return plants


def parse_date(date_str):
    if not date_str:
        return datetime.min
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return datetime.min


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

