from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import users  
import uvicorn
from app.init_db import init


init()
# ---------------------
# Instancia FastAPI
# ---------------------
app = FastAPI(
    title="User Registration API",
    description="API RESTful para registro de usuarios con validaciones",
    version="1.0.0",
)

# ---------------------
# Middleware CORS
# ---------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Enrutadores
# ---------------------
app.include_router(users, tags=["Usuarios"])

# ---------------------
# Manejo global personalizado de errores
# ---------------------

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={"mensaje": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"mensaje": "Datos inválidos en la solicitud."},
    )

# ---------------------
# Punto de entrada para desarrollo local con uvicorn
# ---------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
