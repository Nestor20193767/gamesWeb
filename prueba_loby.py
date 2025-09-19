import random, string
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Diccionario para guardar salas y jugadores
rooms = {}

# --- Generar key aleatoria ---
def generate_key(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# --- Rutas ---
@app.route("/")
def index():
    return render_template("lobys.html")
@app.route("/create_room", methods=["POST"])
def create_room():
    key = generate_key()
    rooms[key] = []
    return jsonify({"key": key})

# --- Eventos Socket.IO ---
@socketio.on("join")
def handle_join(data):
    key = data.get("key")
    name = data.get("name")

    if key not in rooms:
        emit("error", {"msg": "La sala no existe"})
        return

    # Guardar jugador en la sala (si no estaba)
    if name not in rooms[key]:
        rooms[key].append(name)

    join_room(key)

    # Enviar la lista de jugadores actualizada
    emit("joined", {"key": key, "players": rooms[key]}, room=request.sid)
    emit("player_joined", {"players": rooms[key]}, room=key)

@socketio.on("message")
def handle_message(data):
    key = data.get("key")
    msg = data.get("msg")
    name = data.get("name")

    if not key or not msg or not name:
        return

    # Reenviar mensaje a todos en la sala
    emit("message", {"msg": msg, "name": name}, room=key)

# --- Iniciar servidor ---
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
