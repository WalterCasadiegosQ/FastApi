from fastapi import FastAPI, Request
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Leer las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
AUTOR = os.getenv("AUTOR", "Desconocido")

# Configuración SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la tabla notas
class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)

# Crear tablas en la BD
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Notas con FastAPI y PostgreSQL!"}

@app.get("/autor")
async def get_autor():
    return {"autor": AUTOR}

@app.get("/notas-db")
async def get_notas():
    db = SessionLocal()
    notas = db.query(Nota).all()
    db.close()
    return {"notas": [n.contenido for n in notas]}

@app.post("/notas-db")
async def create_nota(request: Request):
    data = await request.json()
    contenido = data.get("contenido")
    db = SessionLocal()
    nueva_nota = Nota(contenido=contenido)
    db.add(nueva_nota)
    db.commit()
    db.close()
    return {"message": "Nota guardada en la base de datos!"}
