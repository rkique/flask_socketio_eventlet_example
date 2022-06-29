from flask_socketio import SocketIO, send, join_room, leave_room
from flask import Flask, render_template
from application import create_app
import eventlet
import logging


app = create_app()
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

assignments = {}
#routes
@app.route('/')
def index():
    return render_template('index.html')

#sockets
@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('join')
def on_join(data):
    username = data['username']
    #compare against assignments before this point
    #if username already in a room, reject
    print(assignments)
    room = data['room']
    if (username in assignments.keys()):
        print("You are in a room.")
        if (assignments[username] == room):
            print("You're already in this room!")
        else:
          print("Leave your current room first before joining this one.")      
    else: 
        assignments[username] = room
        join_room(room)
        send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)
    if (username in assignments.keys()):
        if (assignments[username] == room):
            print("Left the current room.")
            del assignments[username]


if __name__ == '__main__':
    #FLASK RUN does NOT call APP.PY...
    logging.basicConfig(level=logging.ERROR)
    socketio.run(app, port=8000, log_output=False, debug=False)