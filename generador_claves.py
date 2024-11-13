import secrets

def generate_password(length=50):
    """Genera una contraseña aleatoria de la longitud especificada."""
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Generar una contraseña de 32 caracteres
password = generate_password()
print(password)