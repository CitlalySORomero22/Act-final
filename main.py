import databases

import sqlalchemy
from sqlalchemy import Table, Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import select, insert, update, delete


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI() 

DATABASE_URL    =   "sqlite:///clientes.db"

metadata        =   MetaData() 

  
           
clientes = Table(
    "clientes", metadata,
    Column("id_cliente", Integer, primary_key=True),
    Column("nombre", String),
    Column("email", String)
)

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)

class Respuesta (BaseModel) :  
    message: str

class Cliente (BaseModel):  
    id_cliente: int  
    nombre: str  
    email: str  

class ClienteIN (BaseModel):   
    nombre: str  
    email: str 

@app.get("/", response_model=Respuesta) 
async def index(): 
    return {"message": "API REST"} 

@app.get("/clientes/", 
    response_model=List[Cliente],
    summary="Regresa una lista de clientes",
    description="Regresa una lista de clientes"
)
async def get_clientes():
    query = select(clientes)
    return await database.fetch_all(query)


@app.get("/clientes/{id_cliente}", 
    response_model=Cliente,
    summary="Regresa una lista de clientes",
    description="Regresa una lista de clientes"
)
async def get_cliente(id_cliente:int):
    query = select(clientes).where(clientes.c.id_cliente == id_cliente)
    return await database.fetch_one(query)

@app.post("/clientes", response_model=Respuesta) 
async def create_cliente(cliente:ClienteIN):
    query = insert(clientes).values(nombre=cliente.nombre, email=cliente.email)
    await database.execute(query)
    return {"message": "Cliente creado"}


@app.put("/clientes/{id_cliente}", 
    response_model=Respuesta,
    summary="Actualiza un cliente",
    description="Actualiza un cliente"
)

async def update_cliente(id_cliente:int, cliente:ClienteIN):
    query = update(clientes).where(clientes.c.id_cliente == id_cliente).values(nombre=cliente.nombre, email=cliente.email)
    await database.execute(query)
    return {"message": "Cliente actualizado"}

@app.delete("/clientes/{id_cliente}",
    response_model=Respuesta,
    summary="Elimina un cliente",
    description="Elimina un cliente"
)
async def delete_cliente(id_cliente:int):
    query = delete(clientes).where(clientes.c.id_cliente == id_cliente)
    await database.execute(query)
    return {"message": "Cliente eliminado"}