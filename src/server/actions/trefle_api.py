import os
import httpx
import jsonpickle

async def get_all_species():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://trefle.io/api/v1/plants",
            params={"token": os.getenv("API_KEY")}
        )
    resp.raise_for_status()
    return jsonpickle.decode(resp.text)


async def get_species_by_id(species_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://trefle.io/api/v1/species/{species_id}",
            params={"token": os.getenv("API_KEY")}
        )
    resp.raise_for_status()
    return jsonpickle.decode(resp.text)