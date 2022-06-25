from flask_socketio import SocketIO, send, join_room, leave_room
from flask import Flask, render_template
from application import create_app


app = create_app()
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

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
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)


if __name__ == '__main__':
    socketio.run(app)
