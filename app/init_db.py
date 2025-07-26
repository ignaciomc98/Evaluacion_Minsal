from app.database import Base, engine
from app.models import user, phone

def init():
    print("Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)
