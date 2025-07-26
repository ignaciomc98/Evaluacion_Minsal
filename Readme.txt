# 🧪 API RESTful de Registro de Usuarios

Esta es una API RESTful desarrollada con **FastAPI**, que permite registrar usuarios con validaciones, JWT, almacenamiento en SQLite y despliegue mediante Docker.

## 🚀 Requisitos

- Docker y Docker Compose
- Python 3.10+ (solo si deseas correrlo sin contenedor)

## 📦 Instalación con Docker (recomendado)

```
docker-compose up --build
```

La API estará disponible en:  
👉 http://localhost:8000  
Swagger docs: http://localhost:8000/docs

## 🛠️ Estructura del proyecto

```
user_api/
├── app/
│   ├── main.py            # Entry point de la API
│   ├── database.py        # Configuración de la base de datos
│   ├── models/            # Modelos SQLAlchemy (User, Phone)
│   ├── routes/            # Rutas (registro de usuario)
│   ├── schemas/           # Esquemas Pydantic (UserCreate, UserResponse)
│   ├── tests/             # Pruebas Pytest
├── init_db.py             # Inicializa la base de datos
├── test.db                # Base SQLite (persistente en volumen Docker)
├── Dockerfile             # Imagen de la API
├── docker-compose.yml     # Servicio API
├── requirements.txt       # Dependencias
└── README.md              # Este archivo
```

## 🧪 Tests

Usa Pytest para probar el endpoint de registro:

```
pytest
```

Incluye pruebas para:

- Registro exitoso
- Validación de correo
- Validación de contraseña
- Duplicado de email
- Campos faltantes

## 🧾 Especificaciones cumplidas

- ✅ Registro de usuario con JWT
- ✅ Almacena `token`, `created`, `modified`, `last_login`
- ✅ Validación de email (`.cl`, `.com`, `.org`)
- ✅ Validación de contraseña (una mayúscula, letras minúsculas, dos números)
- ✅ Retorna:
  - id (UUID)
  - created
  - modified
  - last_login
  - token (JWT)
  - is_active
- ✅ Persistencia con SQLite (`sqlite:///./test.db`)
- ✅ API contenida en Docker
- ✅ Pruebas unitarias con Pytest
- ✅ Diagrama de arquitectura incluido (`docs/diagrama.png`)

## 📄 Endpoint

### POST `/register`

Registra un nuevo usuario.

**Request JSON:**
```json
{
  "name": "Juan Rodriguez",
  "email": "juan@rodriguez.cl",
  "password": "Password22",
  "phones": [
    {
      "number": "1234567",
      "citycode": "1",
      "countrycode": "57"
    }
  ]
}
```

**Response JSON:**
```json
{
  "id": "uuid",
  "created": "timestamp",
  "modified": "timestamp",
  "last_login": "timestamp",
  "token": "JWT",
  "is_active": true,
  "name": "Juan Rodriguez",
  "email": "juan@rodriguez.cl",
  "phones": [
    {
      "number": "1234567",
      "citycode": "1",
      "countrycode": "57"
    }
  ]
}
```

## 👤 Autor

Ignacio Medina — Desarrollado como parte de una evaluación técnica.

---

### 📎 Notas adicionales

- ⚠️ Si cambias el nombre del archivo `.db`, también actualiza la ruta en `database.py`
- 🧠 Asegúrate de ejecutar `init_db.py` si decides correrlo sin Docker
