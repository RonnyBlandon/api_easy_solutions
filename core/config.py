import json
from fastapi import HTTPException

# SECURITY WARNING: keep the secret key used in production secret!
with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name: str, secrets: dict = secret) -> str:
    try:
        return secrets[secret_name]
    except KeyError:
        # Throws an HTTP exception if the variable is not found
        msg = f"The variable {secret_name} does not exist"
        raise HTTPException(status_code=500, detail=msg)

SECRET_KEY = get_secret("SECRET_KEY")
DATABASE_URL = get_secret("DATABASE_URL")
ACCESS_TOKEN_EXPIRE_MINUTES = get_secret("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = get_secret("ALGORITHM")