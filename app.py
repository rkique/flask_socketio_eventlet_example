from flask_socketio import SocketIO, send
from flask import Flask, render_template
from application import create_app
from application import routes

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

if __name__ == '__main__':
    socketio.run(app)
