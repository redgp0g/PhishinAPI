from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI()

@app.get("/",response_class=HTMLResponse)
def read_root():
    return "Olá mundo!"

@app.get("/registrar-clique")
async def registrar_clique(request: Request, nome: str = None, identificador: str = None, ip: str = None):
    if not nome:
        raise HTTPException(status_code=400, detail="Parâmetros obrigatórios ausentes")

    return JSONResponse(content={
        "mensagem": "Clique registrado com sucesso",
        "nome": nome,
        "identificador": identificador,
        "ip": request.client.host
    })
