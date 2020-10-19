import os
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/chat')
def chat():
    room = request.args.get('room')
    username = request.args.get('username')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@socketio.on('join_room')
def handle_join_room_event(data):
    """
    Using sockets the room id will be passed into join_room to create a new room.
    """
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)    

@socketio.on('send_message')
def handle_send_message_event(data):
    """
    From the created room, when a message is sent the socketio.emit() function can take 3 arguments.
    The last one being the room the message needs to be sent to.
    """
    app.logger.info("{} has sent a message to room {}: {}".format(data['username'], data['room'], data['message']))
    socketio.emit('receive_message', data, room=data['room'])
    

    


if __name__ == "__main__":
    socketio.secret_key = "mysecret"
    socketio.run(app, host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")), debug=True)
