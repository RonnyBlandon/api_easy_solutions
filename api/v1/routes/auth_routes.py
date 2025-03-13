import requests
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas.auth_schemas import GoogleSignInRequest, GoogleSignInResponse, SignInRequest, RefreshToken, Token, PasswordResetRequest
from schemas.user_schemas import UserSchemaCreate
from core.config import get_secret
from database.models.users_model import AuthProviderEnum, User
from database.session import get_db  # Para interactuar con la base de datos
from sqlalchemy.orm import Session
from utils.email_utils import send_email
from core.auth import (create_access_token, create_refresh_token, decode_refresh_token, hash_password, 
                       verify_password, create_password_reset_token, verify_password_reset_token)
from utils.validators import validate_phone_number

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")

# Configura el directorio de las plantillas
templates = Jinja2Templates(directory="templates")


# Endpoint para iniciar sesión en Swagger UI con OAuth2PasswordRequestForm
@router.post("/oauth2-signIn", response_model=Token)
def oauth2_sign_in(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.username).first()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convertir los roles a sus valores (o nombres) antes de crear el token
    roles = [role.value for role in user.roles]

    access_token = create_access_token(data={"id": str(user.id), "roles": roles})
    refresh_token = create_refresh_token(data={"id": str(user.id), "roles": roles})

    return {
        "local_id": str(user.id),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "roles": user.roles
    }

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

    # Convertir los roles a sus valores (o nombres) antes de crear el token
    roles = [role.value for role in user.roles]

    access_token = create_access_token(data={"id": str(user.id), "roles": roles})
    refresh_token = create_refresh_token(data={"id": str(user.id), "roles": roles})

    return {
        "local_id": str(user.id),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "roles": user.roles
    }

# Endpoint para registrar un nuevo usuario
@router.post("/signUp", response_model=Token)
def sign_up(user_data: UserSchemaCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya está registrado"
        )
    # Validación del telefono
    validate_phone_number(user_data.phone_number)

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
        municipality_id=user_data.municipality_id,
        hashed_password=hashed_password,
        providers=['EMAIL'],
        roles=["USER"]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Obtener todos los roles del usuario desde la relación con UserRoleAssociation y Role
    roles = [role.value for role in user.roles]

    access_token = create_access_token(data={"id": str(new_user.id), "roles": roles})
    refresh_token = create_refresh_token(data={"id": str(new_user.id), "roles": roles})

    return {
        "local_id": str(new_user.id),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "roles": user.roles
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

    # Obtener todos los roles del usuario desde la relación con UserRoleAssociation y Role
    roles = [role.value for role in user.roles]

    access_token = create_access_token(data={"id": str(user.id), "roles": roles})
    new_refresh_token = create_refresh_token(data={"id": str(user.id), "roles": roles})

    return {
        "local_id": str(user.id),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
        "roles": user.roles
    }

# Endpoint para solicitar recuperación de contraseña
@router.post("/request-password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email no encontrado")

    # Genera el token de recuperación
    token = create_password_reset_token({"user_id": str(user.id)}, timedelta(minutes=get_secret("RESET_PASSWORD_TOKEN_EXPIRATION_MINUTES")))
    reset_link = f"http://192.168.0.3:8000/auth/reset-password-form?token={token}"

    # Crea el contenido del correo
    email_subject = "Gestión de contraseña"

    email_content = f"""
    <p>Hola {user.full_name},</p>
    <p>Has solicitado actualizar tu contraseña. Haz clic en el siguiente enlace para continuar con el proceso:</p>
    <p><a href="{reset_link}">Cambiar Contraseña</a></p>
    <p>Este enlace es válido por 15 minutos. Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
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
@router.post("/googleSignIn", response_model=GoogleSignInResponse)
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
    email = user_info["email"]
    name = user_info.get("name", "Usuario de Google")

    # Verificar si el usuario ya existe en la base de datos
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Agregar GOOGLE al array de providers si no está presente
        if AuthProviderEnum.GOOGLE not in user.providers:
            user.providers.append(AuthProviderEnum.GOOGLE)
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
            providers=['GOOGLE'],
            roles=["USER"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Obtener todos los roles del usuario desde la relación con UserRoleAssociation y Role
    roles = [role.value for role in user.roles]

    # Crear tokens de acceso y actualización para el usuario
    access_token = create_access_token(data={"id": str(user.id), "roles": roles})
    refresh_token = create_refresh_token(data={"id": str(user.id), "roles": roles})

    return {
        "local_id": str(user.id),
        "full_name": str(user.full_name),
        "email": str(user.email),
        "phone_number": str(user.phone_number),
        "start_date": str(user.start_date),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "providers": user.providers,
        "roles": user.roles
    }
