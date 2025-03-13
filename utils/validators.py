import re
from fastapi import HTTPException

def validate_phone_number(phone_number: str) -> bool:
    """Valida si un número es válido en Honduras (sin código +504)."""
    regex = re.compile(r'^[389]\d{3}[-\s]?\d{4}$')
    if not regex.match(phone_number):
        raise HTTPException(status_code=400, detail="Número de teléfono inválido para Honduras.")
    return True
