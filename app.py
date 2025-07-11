import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Diccionario para manejar múltiples sesiones por usuario
conversaciones = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chatear():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    session_id = data.get("session_id", "default")

    # Crear historial de conversación si no existe
    if session_id not in conversaciones:
        conversaciones[session_id] = [{
            "role": "system",
            "content": "Eres una psicóloga llamada Thea, joven, cercana, relajada y cariñosa. Escribes respuestas cortas, amables y casuales. Al iniciar, pide el nombre del usuario para una conversación más cercana."
        }]

    conversaciones[session_id].append({"role": "user", "content": mensaje})

    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversaciones[session_id]
        )
        respuesta_ia = respuesta.choices[0].message.content
        conversaciones[session_id].append({"role": "assistant", "content": respuesta_ia})

        return jsonify({"respuesta": respuesta_ia})
    except Exception as e:
        return jsonify({"respuesta": "Lo siento, hubo un error 😥"}), 500

if __name__ == "__main__":
    app.run(debug=True)