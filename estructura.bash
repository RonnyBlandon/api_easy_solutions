api_easy_solutions/
├── api/
│   ├── v1/
│   │   ├── routes/
│   │   │   ├── auth.py                # Endpoints de autenticación
│   │   │   ├── customers.py
│   │   │   ├── drivers.py
│   │   │   ├── business_admin.py
│   │   │   ├── business.py
│   │   │   ├── segment.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   ├── invoice.py
├── core/
│   ├── config.py
│   ├── security.py                    # Lógica de seguridad (JWT, hashing de contraseñas)
│   ├── auth.py                        # Servicios de autenticación
├── crud/
│   ├── customer.py
│   ├── driver.py
│   ├── business_admin.py
│   ├── business.py
│   ├── segment.py
│   ├── product.py
│   ├── order.py
│   ├── invoice.py
├── db/
│   ├── base.py
│   ├── models/
│   │   ├── customer.py
│   │   ├── driver.py
│   │   ├── business_admin.py
│   │   ├── business.py
│   │   ├── segment.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── invoice.py
│   ├── session.py
├── schemas/
│   ├── token.py
│   ├── customer.py
│   ├── driver.py
│   ├── business_admin.py
│   ├── business.py
│   ├── segment.py
│   ├── product.py
│   ├── order.py
│   ├── invoice.py
├── services/
│   ├── google_sign_in.py              # Ejemplo de integración con Google
│   ├── apple_sign_in.py               # Ejemplo de integración con Apple
├── helpers/
│   ├── __init__.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── hashing.py
│   │   ├── jwt.py
│   │   └── validation.py
│   └── utils.py                     # Funciones auxiliares y utilitarias
├── main.py
├── alembic/
├── secret.json
├── tests/
├── requirements.txt
