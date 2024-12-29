from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes.auth_routes import router as auth_routes
from api.v1.routes.business_routes import router as business_routes
from api.v1.routes.favourite_routes import router as favourites_router
from database.session import init_db
# import models
from database.models.users_model import User, UserRole, Driver, BusinessAdmin, Department, Municipality, Address
from database.models.business_model import TypeBusiness, Business
from database.models.product_model import Category, Product, Option, Extra
from database.models.image_model import Image
from database.models.favourite_model import Favourite

# Inicializa la base de datos
init_db()

app = FastAPI(title="Easy Solutions API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas de autenticación
app.include_router(auth_routes)
app.include_router(business_routes)
app.include_router(favourites_router)

@app.get("/")
def root():
    return {"message": "Hi, I am fastapi."}
