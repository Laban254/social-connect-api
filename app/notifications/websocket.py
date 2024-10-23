from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
from app.utils.auth import get_current_user_id 

# Set custom ping timeout and interval
socketio = SocketIO(ping_timeout=60, ping_interval=25)

connected_clients = {}

@socketio.on('connect')
def handle_connect():
    user_id = get_current_user_id()
    if user_id:
        connected_clients[user_id] = request.sid
        print(f"User {user_id} connected with session ID: {request.sid}")
        socketio.emit('message', {'data': 'Connected to notifications service'})
    else:
        print("Unauthorized connection attempt.")

@socketio.on('disconnect')
def handle_disconnect():
    user_id = get_current_user_id()
    if user_id and user_id in connected_clients:
        del connected_clients[user_id]
        print(f"User {user_id} disconnected.")

def send_notification(user_id, message):
    print(f"Sending notification to user_id: {user_id} with message: {message}")
    if user_id in connected_clients:
        socketio.emit('notification', {'message': message}, room=connected_clients[user_id])
        print(f"Notification sent to user {user_id}.")
    else:
        print(f"User {user_id} not connected. Notification not sent.")
