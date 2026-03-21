from fastapi import FastAPI
from dotenv import load_dotenv

from src.server.database.databaseConnection import initialize

# Import routers (we’ll create these next)
from routes import auth, plants, pages

app = FastAPI()
load_dotenv()

@app.on_event("startup")
def startup_event():
    initialize()

# Register routes
app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(pages.router)