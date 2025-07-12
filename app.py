import os
import uuid
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from openai import OpenAI

# Inicializa Flask
app = Flask(__name__)

# Configuración de la sesión
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Cliente de OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Función para obtener o crear el contexto del usuario
def get_user_context():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
        session["contexto"] = [{
            "role": "system",
            "content": "Eres una psicóloga llamada Thea, joven, cercana, relajada y cariñosa. Escribes respuestas cortas, amables y casuales. Al iniciar, pide el nombre del usuario para una conversación más cercana."
        }]
    return session["contexto"]

# Ruta principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta del chat
@app.route("/chat", methods=["POST"])
def chatear():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    
    contexto = get_user_context()
    contexto.append({"role": "user", "content": mensaje})

    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=contexto
    )

    respuesta_ia = respuesta.choices[0].message.content
    contexto.append({"role": "assistant", "content": respuesta_ia})
    session["contexto"] = contexto  # Guarda el contexto actualizado en la sesión

    return jsonify({"respuesta": respuesta_ia})

# Ejecutar en modo desarrollo (no se usa en Render)
if __name__ == "__main__":
    app.run(debug=True)