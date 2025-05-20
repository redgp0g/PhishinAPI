import datetime
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pytz import timezone

app = FastAPI()
stringConnection = os.getenv("MONGO_CONNECTION")

if not stringConnection:
    raise RuntimeError("A variável de ambiente MONGO_CONNECTION não está definida.")

uri = stringConnection

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.phishing_sch

phishing = db["phishing"]


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "Olá mundo!"

@app.get("/registrar-clique", response_class=JSONResponse)
async def registrar_clique(request: Request, nome: str = None):
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
