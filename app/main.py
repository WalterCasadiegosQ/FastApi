from fastapi import FastAPI, Request
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#Direccion archivo plano
DATA_FILE = "/data/notas.txt"

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

# GET - obtener autor
@app.get("/autor")
async def get_autor():
    return {"autor": AUTOR}

# GET - obtener nota BD
@app.get("/notas-db")
async def get_notas():
    db = SessionLocal()
    notas = db.query(Nota).all()
    db.close()
    return {"notas": [n.contenido for n in notas]}

# POST - agregar nota BD
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

# POST - agregar una nota
@app.post("/nota")
async def guardar_nota(request: Request):
    nota = await request.body()
    with open(DATA_FILE, "a") as f:
        f.write(nota.decode() + "\n")
    return {"mensaje": "Nota guardada"}

# GET - obtener todas las notas
@app.get("/notas")
def leer_notas():
    if not os.path.exists(DATA_FILE):
        return {"notas": []}
    with open(DATA_FILE, "r") as f:
        return {"notas": f.read().splitlines()}

# GET - contar cantidad de notas
@app.get("/conteo")
def contar_notas():
    if not os.path.exists(DATA_FILE):
        return {"conteo": 0}
    with open(DATA_FILE, "r") as f:
        return {"conteo": len(f.readlines())}