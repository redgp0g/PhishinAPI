import datetime
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pytz import timezone

app = FastAPI()
stringConnection = os.environ.get("MONGO_CONNECTION")

uri = stringConnection

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.phishing_sch

phishing = db["phishing"]


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "Olá "+ os.environ.get('TESTE') + ", você está no servidor de phishing!"

@app.get("/registrar-clique", response_class=JSONResponse)
async def registrar_clique(request: Request, nome: str = None):
    try:
        if not stringConnection:
            raise HTTPException(status_code=500, detail="Conexão com o banco de dados não configurada.")
        ip = request.client.host
        brasilia = timezone('America/Sao_Paulo')
        now = datetime.datetime.now(brasilia)

        clique = {
            "nome": nome,
            "ip": ip,
            "data_hora": now
        }
        resultado = phishing.insert_one(clique)
        return {
            "id": str(resultado.inserted_id),
            "nome": nome,
            "ip": ip,
            "data_hora": now
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
