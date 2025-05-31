from fastapi import FastAPI , WebSocket,WebSocketDisconnect,Request
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware
from elrahapi.websocket.connection_manager import ConnectionManager
# from .myapp.router import app_myapp
from .settings.database import database
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates=Jinja2Templates(directory="learning_websocket/templates")


@app.get("/hello")
async def hello():
    return {"message": "hello"}

@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

manager=ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(message=data)
    except WebSocketDisconnect:
        await manager.disconnect(webSocket=websocket)
        await manager.broadcast(message="Un utilisateur s'est déconnecté")


# app.include_router(app_myapp)
app.add_middleware(
    ErrorHandlingMiddleware,
)
