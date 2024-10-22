from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
from app.utils.auth import get_current_user_id 

connected_clients = {}

@socketio.on('connect')
def handle_connect():
    user_id = get_current_user_id() 
    if user_id:
        connected_clients[user_id] = request.sid  # Store the connection ID for the user
        emit('message', {'data': 'Connected to notifications service'})

@socketio.on('disconnect')
def handle_disconnect():
    user_id = get_current_user_id()
    if user_id and user_id in connected_clients:
        del connected_clients[user_id]

def send_notification(user_id, message):
    if user_id in connected_clients:
        socketio.emit('notification', {'message': message}, room=connected_clients[user_id])
