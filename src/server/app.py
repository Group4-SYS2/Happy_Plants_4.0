from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.routing import RedirectResponse

from fastapi import FastAPI, Request, Form, status

from database.databaseConnection import loginUser, registerUser, getAllUsers, initialize, getCurrentUser, signOutUser, \
    getUserPlants, deleteUserPlant

# Starts the fastapi RESTful api
app = FastAPI()

# Mounts the app to a path, reason unclear
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define where the templates are stored
templates = Jinja2Templates(directory="templates")

# Starts the database client
initialize()

@app.get("/home")
async def home(request: Request):
    current_user = getCurrentUser()

    if current_user is not None:
        print("found user")
        return templates.TemplateResponse("main.tpl", {"request": request, "email": current_user.user.email})
    else:
        print("no user found")
        return templates.TemplateResponse("login.tpl", {"request": request})

@app.get("/logout")
async def logout(request: Request):
    signOutUser()

    # Redirects user to the home page,
    # status_code is 303 because that makes the redirect request a GET request
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
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
    user_id = current_user.user.id

    plants = getUserPlants(user_id)

    return templates.TemplateResponse("myPlants.tpl", {"request": request, "plants" : plants, "email": current_user.user.email})

@app.delete("/myPlants/delete/{plant_id}")
async def myPlantDelete(request: Request, plant_id: int):
    current_user = getCurrentUser()
    user_id = current_user.user.id
    deleteUserPlant(plant_id, user_id)