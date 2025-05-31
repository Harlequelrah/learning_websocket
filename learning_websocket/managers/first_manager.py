from fastapi import WebSocket
class MyFirstConnectionManager():
    def __init__(self):
        self.active_connections:dict[WebSocket:str]={}

    async def connect(self,websocket:WebSocket,username:str):
        await websocket.accept()
        self.active_connections[websocket]=username
        await self.broadcast(f"{username} vient de rejoindre le chat")

    async def disconnect(self,websocket:WebSocket):
        username = self.get_username(websocket=websocket)
        self.active_connections.pop(websocket,None)
        return username


    async def broadcast(self,message:str):
        for connection in self.active_connections:
                await connection.send_text(message)

    async def send_message(self,websocket:WebSocket,message:str):
        for connection in self.active_connections:
            if connection!=websocket:
                await connection.send_text(message)

    def get_username(self,websocket:WebSocket):
        return self.active_connections.get(websocket,"Utilisateur inconnu")


