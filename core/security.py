from fastapi import Security, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.auth import decode_access_token
from schemas.auth_schemas import TokenData  # Importamos TokenData desde el nuevo archivo

# Definición del esquema de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/oauth2-signIn")

# Obtener el usuario actual a partir del token
def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    return decode_access_token(token)

# Verificar que el usuario esté activo
def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    if not current_user.local_id:  # Verifica que el usuario tenga un ID válido
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo o inválido")
    return current_user

# Verificar que el usuario tenga un rol específico
def get_current_user_with_role(required_roles: str):
    def role_verification(current_user: TokenData = Depends(get_current_active_user)) -> TokenData:
        if current_user.roles != required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"El usuario no tiene privilegios de {required_roles}"
            )
        return current_user
    return role_verification

# Funciones para verificar roles específicos
def get_current_admin_user(current_user: TokenData = Depends(get_current_user_with_role("business_admin"))) -> TokenData:
    return current_user

def get_current_driver_user(current_user: TokenData = Depends(get_current_user_with_role("driver"))) -> TokenData:
    return current_user

def get_current_customer_user(current_user: TokenData = Depends(get_current_user_with_role("customer"))) -> TokenData:
    return current_user

def get_current_superadmin_user(current_user: TokenData = Depends(get_current_user_with_role("super_admin"))) -> TokenData:
    return current_user
