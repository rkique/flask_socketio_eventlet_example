# Flask-SocketIO and Eventlet Chat App

This is a working example of a chat application built with `flask`, `flask_socketio`, and `eventlet`. Initially I was very confused about the servers and frameworks, here's what I learned so far: 

- There are two python modules `flask_socketio` and  `python-socketio`. Python-socketio worked with waitress but not with eventlet. Both help python interface with socketio.

- eventlet is a server
    - like gunicorn (not windows-compatible) 
    - and like waitress (windows-compatible, but hard to run from the commandline, and can't handle WebSockets)

... and it has Websocket support

Okay cool. Now I'm going to extend this to work with golf.
