from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes.auth_routes import router as auth_routes
from database.session import init_db

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
app.include_router(auth_routes, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Hi, I am fastapi."}
