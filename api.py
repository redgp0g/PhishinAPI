from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/",response_class=HTMLResponse)
def read_root():
    return "Olá mundo!"

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)    