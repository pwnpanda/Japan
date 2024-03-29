from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='')
io = SocketIO(app)

clients = []

@app.route('/')
def index():
    return app.send_static_file('client.html')
    
@io.on('connected')
def connected():
	print("Here!")
	print "%s connected" % (request.namespace.socket.sessid)
	clients.append(request.namespace)
    
@io.on('disconnect')
def disconnect():
	print("Here2!")
	print "%s disconnected" % (request.namespace.socket.sessid)
	clients.remove(request.namespace)
    
def hello_to_random_client():
    import random
    from datetime import datetime
    if clients:
        k = random.randint(0, len(clients)-1)
        print "Saying hello to %s" % (clients[k].socket.sessid)
        clients[k].emit('message', "Hello at %s" % (datetime.now()))

if __name__ == '__main__':
	import time

	io.run(app)
	
	time.sleep(15)
	hello_to_random_client()