import requests
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas.auth_schemas import GoogleSignInRequest, SignInRequest, RefreshToken, Token, PasswordResetRequest
from schemas.user_schemas import UserCreateSchema
from core.config import get_secret
from database.models.users_model import User
from database.session import get_db  # Para interactuar con la base de datos
from sqlalchemy.orm import Session
from utils.email_utils import send_email
from core.auth import (create_access_token, create_refresh_token, decode_refresh_token, hash_password, 
                       verify_password, create_password_reset_token, verify_password_reset_token)

router = APIRouter()

GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")

# Configura el directorio de las plantillas
templates = Jinja2Templates(directory="templates")

# Endpoint para iniciar sesión
@router.post("/signIn", response_model=Token)
def sign_in(data: SignInRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"id": str(user.id), "role": str(user.role)})
    refresh_token = create_refresh_token(data={"id": str(user.id), "role": str(user.role)})

    return {
        "local_id": str(user.id),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "role": str(user.role)
    }

# Endpoint para registrar un nuevo usuario
@router.post("/signUp", response_model=Token)
def sign_up(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya está registrado"
        )

    # Validación de la contraseña
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres"
        )

    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        phone_number=user_data.phone_number,
        full_name=user_data.full_name,
        department_id=user_data.department_id,
        municipality_id=user_data.municipality_id,
        hashed_password=hashed_password,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"id": str(new_user.id), "role": str(new_user.role)})
    refresh_token = create_refresh_token(data={"id": str(new_user.id), "role": str(new_user.role)})

    return {
        "local_id": str(new_user.id),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "role": str(new_user.role)
    }

# Endpoint para renovar el access token usando el refresh token
@router.post("/refreshToken", response_model=Token)
def refresh_token(refresh_token: RefreshToken, db: Session = Depends(get_db)):
    token_data = decode_refresh_token(refresh_token.refresh_token)
    user = db.query(User).filter(User.id == token_data.local_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    access_token = create_access_token(data={"id": str(user.id), "role": str(user.role)})
    new_refresh_token = create_refresh_token(data={"id": str(user.id), "role": str(user.role)})

    return {
        "local_id": str(user.id),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
        "role": str(user.role)
    }

# Endpoint para solicitar recuperación de contraseña
@router.post("/request-password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email no encontrado")

    # Genera el token de recuperación
    token = create_password_reset_token({"user_id": str(user.id)}, timedelta(minutes=get_secret("RESET_PASSWORD_TOKEN_EXPIRATION_MINUTES")))
    reset_link = f"http://192.168.0.7:8000/auth/reset-password-form?token={token}"

    # Crea el contenido del correo
    email_subject = "Recuperación de contraseña"
    email_content = f"""
    <p>Hola {user.full_name},</p>
    <p>Parece que solicitaste la recuperación de tu contraseña. Haz clic en el siguiente enlace para restablecer tu contraseña:</p>
    <p><a href="{reset_link}">Restablecer Contraseña</a></p>
    <p>Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
    """

    # Envía el correo electrónico
    send_email(subject=email_subject, recipient=user.email, html_content=email_content)

    return {"msg": "Enlace de recuperación de contraseña enviado a tu correo"}

# Endpoint para renderizar el formulario para agregar la nueva contraseña
@router.get("/reset-password-form", response_class=HTMLResponse)
async def get_reset_password_form(token: str, request: Request):
    return templates.TemplateResponse("reset_password_form.html", {"request": request, "token": token})

# Endpoint para confirmar la recuperación de contraseña
@router.post("/reset-password", response_class=HTMLResponse)
async def reset_password(
    request: Request,
    token: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Verifica el token y obtiene la información del usuario
    payload = verify_password_reset_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido o expirado")

    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    # Validación de la nueva contraseña
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres"
        )

    # Actualiza la contraseña del usuario
    user.hashed_password = hash_password(new_password)
    db.commit()

    return templates.TemplateResponse("password_updated.html", {"request": request, "msg": "Contraseña actualizada exitosamente"})

# Endpoint de GoogleSignIn
@router.post("/googleSignIn")
def google_sign_in(request: GoogleSignInRequest, db: Session = Depends(get_db)):
    # Verifica que el access_token esté presente
    if not request.access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere un access_token de Google."
        )

    # Verificación usando access_token
    response = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={request.access_token}")
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El access_token de Google no es válido",
        )
    user_info = response.json()
    
    # Extraer información del usuario desde el token
    google_user_id = user_info["sub"]
    email = user_info["email"]
    name = user_info.get("name", "Usuario de Google")
    print("Esto contiene user_info: ", user_info)

    # Verificar si el usuario ya existe en la base de datos
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Si el usuario existe pero no tiene google_user_id, actualízalo
        if not user.google_user_id:
            user.google_user_id = google_user_id
            db.commit()
            db.refresh(user)
    else:
        # Si no existe, registrar el usuario
        user = User(
            email=email,
            full_name=name,
            phone_number="",
            department_id=1,
            municipality_id=1,
            is_active=True,
            google_user_id=google_user_id,
            role="USER"  # Asigna el rol correspondiente
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Crear tokens de acceso y actualización para el usuario
    access_token = create_access_token(data={"id": str(user.id), "role": str(user.role)})
    refresh_token = create_refresh_token(data={"id": str(user.id), "role": str(user.role)})

    return {
        "local_id": str(user.id),
        "full_name": str(user.full_name),
        "email": str(user.email),
        "phone_number": str(user.phone_number),
        "start_date": str(user.created_at),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "role": str(user.role)
    }