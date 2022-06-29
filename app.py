from flask_socketio import SocketIO, send, join_room, leave_room
from flask import Flask, render_template, request
from application import create_app
import eventlet
import logging


app = create_app()
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

Users = set()
#routes
@app.route('/')
def index():
    return render_template('index.html')

class User:
    def __init__(self,sid):
        self.sid = sid
        self.room = sid
        self.username = ""
    def __repr__(self):
        return f'sid: {self.sid}, room: {self.room},username: {self.username}'
#sockets
@socketio.on('message')
def handleMessage(msg):
    this_user = User(request.sid)
    if this_user.sid not in [user.sid for user in Users]:
        Users.add(this_user)
        print(f'[New User] Users is {Users}')
    print(f'[Message] {msg} from {request.sid}')
    send(msg, broadcast=True)
    

@socketio.on('join')
def on_join(data):
    username = data['username']
    session_id = data["id"]
    #compare against Users before this point
    #if username already in a room, reject
    print(Users)
    room = data['room']
    if (username in Users.keys()):
        print("You are in a room.")
        if (Users[username] == room):
            print("You're already in this room!")
        else:
          print("Leave your current room first before joining this one.")      
    else: 
        Users[username].room = room
        Users[username].id = session_id
        join_room(room)
        send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)
    if (username in Users.keys()):
        if (Users[username] == room):
            print("Left the current room.")
            del Users[username]

if __name__ == '__main__':
    #FLASK RUN does NOT call APP.PY...
    logging.basicConfig(level=logging.ERROR)
    socketio.run(app, port=8000, log_output=False, debug=False)