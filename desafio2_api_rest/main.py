from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

import json
from typing import List

# --- CONFIGURAÇÃO DO BANCO RELACIONAL (SQLite) ---
URL_BANCO = "sqlite:///./carros.db"
engine = create_engine(URL_BANCO, connect_args={"check_same_thread": False})
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CarroDB(Base):
    __tablename__ = "carros"
    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String)
    modelo = Column(String)
    ano = Column(Integer)
    preco = Column(Float)

Base.metadata.create_all(bind=engine)

class CarroSchema(BaseModel):
    marca: str
    modelo: str
    ano: int
    preco: float

class CarroResposta(CarroSchema):
    id: int
    class Config:
        orm_mode = True

app = FastAPI(title="API de Carros")

def get_db():
    db = SessaoLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS DO BANCO RELACIONAL (CRUD de Carros) ---
@app.post("/carros/", response_model=CarroResposta, status_code=201, tags=["Banco Relacional - Carros"])
def criar_carro(carro: CarroSchema, db: Session = Depends(get_db)):
    db_carro = CarroDB(**carro.dict())
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    return db_carro

@app.get("/carros/{carro_id}", response_model=CarroResposta, tags=["Banco Relacional - Carros"])
def ler_carro(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(CarroDB).filter(CarroDB.id == carro_id).first()
    if carro is None:
        raise HTTPException(status_code=404, detail="carro não encontrado")
    return carro

@app.get("/carros/", response_model=list[CarroResposta], tags=["Banco Relacional - Carros"])
def ler_carros(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    carros = db.query(CarroDB).offset(skip).limit(limit).all()
    return carros

@app.put("/carros/{carro_id}", response_model=CarroResposta, tags=["Banco Relacional - Carros"])
def atualizar_carro(carro_id: int, carro_update: CarroSchema, db: Session = Depends(get_db)):
    db_carro = db.query(CarroDB).filter(CarroDB.id == carro_id).first()
    if db_carro is None:
        raise HTTPException(status_code=404, detail="carro não encontrado")
    for var, value in vars(carro_update).items():
        setattr(db_carro, var, value)
    db.commit()
    db.refresh(db_carro)
    return db_carro

@app.delete("/carros/{carro_id}", status_code=204, tags=["Banco Relacional - Carros"])
def deletar_carro(carro_id: int, db: Session = Depends(get_db)):
    db_carro = db.query(CarroDB).filter(CarroDB.id == carro_id).first()
    if db_carro is None:
        raise HTTPException(status_code=404, detail="carro não encontrado")
    db.delete(db_carro)
    db.commit()
    return

# --- CONFIGURAÇÃO E ENDPOINTS DO BANCO NÃO RELACIONAL (Arquivo JSON) ---
DB_REVISOES_ARQUIVO = "revisoes.json"

class RevisaoSchema(BaseModel):
    descricao: str
    custo: float

# função para ler o "banco" json
def ler_revisoes_db() -> dict:
    try:
        with open(DB_REVISOES_ARQUIVO, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# função para salvar no "banco" json
def salvar_revisoes_db(data: dict):
    with open(DB_REVISOES_ARQUIVO, "w") as f:
        json.dump(data, f, indent=4)

@app.post("/carros/{carro_id}/revisoes", tags=["Banco Não Relacional - Revisões"])
def adicionar_revisao(carro_id: str, revisao: RevisaoSchema):
    db_revisoes = ler_revisoes_db()
    if carro_id not in db_revisoes:
        db_revisoes[carro_id] = []
    
    db_revisoes[carro_id].append(revisao.dict())
    salvar_revisoes_db(db_revisoes)
    return {"status": f"revisão adicionada para o carro {carro_id}"}

@app.get("/carros/{carro_id}/revisoes", response_model=List[RevisaoSchema], tags=["Banco Não Relacional - Revisões"])
def listar_revisoes(carro_id: str):
    db_revisoes = ler_revisoes_db()
    revisoes_carro = db_revisoes.get(carro_id, [])
    if not revisoes_carro:
         raise HTTPException(status_code=404, detail="nenhuma revisão encontrada para este carro")
    return revisoes_carro