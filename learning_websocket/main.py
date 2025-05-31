from fastapi import FastAPI, Query , WebSocket,WebSocketDisconnect,Request
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware
from elrahapi.websocket.connection_manager import ConnectionManager
from .managers.first_manager import MyFirstConnectionManager
from .managers.chat_manager import ChatConnectionManager

# from .myapp.router import app_myapp
from .settings.database import database
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates=Jinja2Templates(directory="learning_websocket/templates")
manager = ConnectionManager()
first_manager = MyFirstConnectionManager()
chat_manager = ChatConnectionManager()

@app.get("/hello")
async def hello():
    return {"message": "hello"}

@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.get("/first_manager", response_class=HTMLResponse)
async def first_manager(request:Request):
    return templates.TemplateResponse("first_manager.html",{"request":request})


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


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

@app.websocket("/ws/{username}")
async def username_websocket_endpoint(username:str,websocket:WebSocket):
    await first_manager.connect(websocket=websocket,username=username)
    try :
        while True:
            data= await websocket.receive_text()
            await first_manager.broadcast(f"{username} : {data}")
    except WebSocketDisconnect:
        await first_manager.disconnect(websocket)
        await first_manager.broadcast(message=f"{username} vient de se déconnecté")

@app.websocket("/ws/room/{room_name}")
async def chat_websocket(websocket:WebSocket,room_name:str,sub:str=Query(...)):
    chat_manager.create_room(room_name=room_name)
    await chat_manager.connect(websocket=websocket,room_name=room_name,sub=sub)
    try:
        while True:
            data= await websocket.receive_text()
            await chat_manager.broadcast(room_name=room_name,message=f"{sub} a dit : {data}")
    except WebSocketDisconnect:
        sub = await chat_manager.disconnect(websocket=websocket,room_name=room_name)
# app.include_router(app_myapp)
app.add_middleware(
    ErrorHandlingMiddleware,
)
