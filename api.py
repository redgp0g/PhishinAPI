import datetime
import os
import pyodbc
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv
from pytz import timezone

app = FastAPI()

@app.get("/")
def root():
    print("Root of Phishing API")
    try:
        conn = get_conn()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT @@version")
        return 'funcionando'
    except Exception as e:
        return {"error": "Erro ao conectar ao banco de dados"}

@app.get("/all")
def get_all_clicks():
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM phishing")
            rows = cursor.fetchall()
            return {"clicks": [dict(zip([column[0] for column in cursor.description], row)) for row in rows]}
    except Exception as e:
        return {"error": "Erro ao conectar ao banco de dados"}

@app.get("/registrar-clique", response_class=JSONResponse)
async def registrar_clique(request: Request, nome: str = None):
    ip = request.client.host
    brasilia = timezone('America/Sao_Paulo')
    now = datetime.datetime.now(brasilia)

    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO phishing (nome, ip, data_hora) VALUES (?, ?, ?)", nome, ip, now)
            conn.commit()

        return {
            "nome": nome,
            "ip": ip,
            "data_hora": now.isoformat()
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao inserir no banco")


def get_conn():
    connection_string = os.environ.get("DB_CONNECTION")
    if not connection_string:
        load_dotenv()
        connection_string = os.getenv("DB_CONNECTION")
    
    if not connection_string:
        raise RuntimeError("A variável de ambiente DB_CONNECTION não está definida.")
    conn = pyodbc.connect(connection_string)
    return conn
