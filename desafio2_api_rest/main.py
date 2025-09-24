# 1: importações das ferramentas necessárias
from fastapi import FastAPI, HTTPException, Depends # framework web
from pydantic import BaseModel # validação de dados
from sqlalchemy import create_engine, Column, Integer, String, Float # ORM
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

import json
from typing import List

# 2: configuração do banco de dados relacional (sqlite)
URL_BANCO = "sqlite:///./carros.db"
engine = create_engine(URL_BANCO, connect_args={"check_same_thread": False})
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3: modelo da tabela do banco (sqlalchemy)
class CarroDB(Base):
    __tablename__ = "carros"
    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String)
    modelo = Column(String)
    ano = Column(Integer)
    preco = Column(Float)

# 4: cria a tabela no banco de dados, se ela não existir
Base.metadata.create_all(bind=engine)

# 5: modelo de dados para validação da entrada (pydantic)
class CarroSchema(BaseModel):
    marca: str
    modelo: str
    ano: int
    preco: float

# 6: modelo de dados para formatação da resposta (pydantic)
class CarroResposta(CarroSchema):
    id: int
    class Config:
        orm_mode = True

# 7: criação da aplicação fastapi
app = FastAPI(title="API de Carros")

# 8: função para gerenciar a sessão com o banco de dados
def get_db():
    db = SessaoLocal()
    try:
        yield db
    finally:
        db.close()

# --- endpoints do banco relacional ---

# endpoint para criar um novo carro
@app.post("/carros/", response_model=CarroResposta, status_code=201, tags=["Banco Relacional - Carros"])
def criar_carro(carro: CarroSchema, db: Session = Depends(get_db)):
    db_carro = CarroDB(**carro.dict())
    db.add(db_carro)
    db.commit()
    db.refresh(db_carro)
    return db_carro

# endpoint para buscar um único carro pelo id
@app.get("/carros/{carro_id}", response_model=CarroResposta, tags=["Banco Relacional - Carros"])
def ler_carro(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(CarroDB).filter(CarroDB.id == carro_id).first()
    if carro is None:
        raise HTTPException(status_code=404, detail="carro não encontrado")
    return carro

# endpoint para listar todos os carros
@app.get("/carros/", response_model=list[CarroResposta], tags=["Banco Relacional - Carros"])
def ler_carros(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    carros = db.query(CarroDB).offset(skip).limit(limit).all()
    return carros

# endpoint para atualizar um carro existente
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

# endpoint para deletar um carro
@app.delete("/carros/{carro_id}", status_code=204, tags=["Banco Relacional - Carros"])
def deletar_carro(carro_id: int, db: Session = Depends(get_db)):
    db_carro = db.query(CarroDB).filter(CarroDB.id == carro_id).first()
    if db_carro is None:
        raise HTTPException(status_code=404, detail="carro não encontrado")
    db.delete(db_carro)
    db.commit()
    return

# --- endpoints do banco não relacional (arquivo json) ---

# 9: define o nome do arquivo que servirá de banco
DB_REVISOES_ARQUIVO = "revisoes.json"

# 10: modelo de dados para validação das revisões (pydantic)
class RevisaoSchema(BaseModel):
    descricao: str
    custo: float

# 11: função auxiliar para ler os dados do arquivo json
def ler_revisoes_db() -> dict:
    try:
        with open(DB_REVISOES_ARQUIVO, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# 12: função auxiliar para salvar os dados no arquivo json
def salvar_revisoes_db(data: dict):
    with open(DB_REVISOES_ARQUIVO, "w") as f:
        json.dump(data, f, indent=4)

# endpoint para adicionar uma nova revisão a um carro (create)
@app.post("/carros/{carro_id}/revisoes", tags=["Banco Não Relacional - Revisões"])
def adicionar_revisao(carro_id: str, revisao: RevisaoSchema):
    db_revisoes = ler_revisoes_db()
    
    if carro_id not in db_revisoes:
        db_revisoes[carro_id] = []
    
    db_revisoes[carro_id].append(revisao.dict())
    salvar_revisoes_db(db_revisoes)
    return {"status": f"revisão adicionada para o carro {carro_id}"}

# endpoint para listar todas as revisões de um carro (read)
@app.get("/carros/{carro_id}/revisoes", response_model=List[RevisaoSchema], tags=["Banco Não Relacional - Revisões"])
def listar_revisoes(carro_id: str):
    db_revisoes = ler_revisoes_db()
    revisoes_carro = db_revisoes.get(carro_id, [])
    if not revisoes_carro:
         raise HTTPException(status_code=404, detail="nenhuma revisão encontrada para este carro")
    return revisoes_carro

# endpoint para atualizar uma revisão específica (update)
@app.put("/carros/{carro_id}/revisoes/{revisao_index}", tags=["Banco Não Relacional - Revisões"])
def atualizar_revisao(carro_id: str, revisao_index: int, revisao: RevisaoSchema):
    db_revisoes = ler_revisoes_db()
    
    if carro_id not in db_revisoes or revisao_index >= len(db_revisoes[carro_id]):
        raise HTTPException(status_code=404, detail="revisão não encontrada")
    
    db_revisoes[carro_id][revisao_index] = revisao.dict()
    salvar_revisoes_db(db_revisoes)
    return {"status": f"revisão {revisao_index} do carro {carro_id} atualizada"}

# endpoint para deletar uma revisão específica (delete)
@app.delete("/carros/{carro_id}/revisoes/{revisao_index}", status_code=204, tags=["Banco Não Relacional - Revisões"])
def deletar_revisao(carro_id: str, revisao_index: int):
    db_revisoes = ler_revisoes_db()

    if carro_id not in db_revisoes or revisao_index >= len(db_revisoes[carro_id]):
        raise HTTPException(status_code=404, detail="revisão não encontrada")

    db_revisoes[carro_id].pop(revisao_index)
    
    # se não houver mais revisões para o carro, remove a chave do carro
    if not db_revisoes[carro_id]:
        del db_revisoes[carro_id]
        
    salvar_revisoes_db(db_revisoes)

    return
