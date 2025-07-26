# app/crud.py
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import HTTPException
from app import models, schemas, auth

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Verificar si el correo ya existe
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail={"mensaje": "El correo ya está registrado"}
        )

    # Hashear contraseña
    hashed_password = auth.get_password_hash(user.password)
    now = datetime.utcnow()

    # Crear token JWT válido por 2 horas
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(hours=2)
    )

    # Crear objeto usuario con UUID y demás campos
    db_user = models.User(
        id=str(uuid4()),
        nombre=user.nombre,
        email=user.email,
        hashed_password=hashed_password,
        created=now,
        modified=now,
        last_login=now,
        token=access_token,
        isactive=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Crear teléfonos asociados si los hay
    if user.phones:
        for phone in user.phones:
            db_phone = models.Phone(
                id=str(uuid4()),
                number=phone.number,
                citycode=phone.citycode,
                countrycode=phone.countrycode,
                user_id=db_user.id,
            )
            db.add(db_phone)
        db.commit()
        db.refresh(db_user)

    return db_user
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_email(db, email=username)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user
