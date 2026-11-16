from flask import request
from flask_socketio import emit

def init_app(socketio):
    #eventos disparados pelo servidor
    @socketio.on("connect")
    def handle_connect():
        print(f"o usuario com o id: {request.sid} se conectou.")
        
    @socketio.on("disconnect")
    def handle_disconnect():
        print(f"o usuario com o id: {request.sid} se desconectou.")
        
        # usuario entrou no chat        
    @socketio.on("join")
    def handle_join(data):
        print(f"o usuario {data['nickname']} entrou no chat.")
        emit("join", data, broadcast=True)
    @socketio.on("msg")
    def hadle_msg(data):
        print(data)
        emit("showmsg", data, broadcast=True)