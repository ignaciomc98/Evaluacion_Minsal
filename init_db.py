# init_db.py

from app.database import Base, engine
from app.models import user, phone  # Importa los modelos para que se registren

print("Usando base de datos en:", engine.url)
print("Creando tablas en la DB...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas.")
