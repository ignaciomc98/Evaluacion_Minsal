from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timezone, timedelta
import jwt
import re
from passlib.context import CryptContext

from app.database import get_db
from app.models import User, Phone
from app.schemas.user import UserCreate, UserResponse

SECRET_KEY = "secret"  # En producción, usar variable de entorno segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()  # ¡IMPORTANTE! Definir antes del uso de @router.post


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Validar formato de correo con dominios permitidos (.cl, .com, .org)
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.(cl|com|org)$", user.email):
        raise HTTPException(
            status_code=422,
            detail="El correo debe tener un dominio válido (.cl, .com, .org)"
        )

    # 2. Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    # 3. Generar UUID y timestamps
    now = datetime.now(timezone.utc)
    user_id = str(uuid4())

    # 4. Hashear password
    hashed_password = hash_password(user.password)

    # 5. Crear token JWT
    token_data = {
        "sub": user_id,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # 6. Crear instancia User
    db_user = User(
        id=user_id,
        name=user.name,
        email=user.email,
        password=hashed_password,
        created=now,
        modified=now,
        last_login=now,
        token=token,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 7. Crear teléfonos asociados
    for phone in user.phones:
        db_phone = Phone(
            number=phone.number,
            citycode=phone.citycode,
            countrycode=phone.countrycode,
            user_id=user_id
        )
        db.add(db_phone)
    db.commit()

    # 8. Refrescar usuario para incluir teléfonos
    db.refresh(db_user)

    return db_user



