from flask import Flask, request, jsonify, render_template, session
import os
from openai import OpenAI
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def obtener_contexto():
    if "user_id" not in session:
        session["user_id"] = str(uuid4())
        session["contexto"] = [
            {
                "role": "system",
                "content": "Eres una psicóloga llamada Thea, joven, cercana, amigable y muy cariñosa. Escribes respuestas cortas, amables y casuales. Al iniciar, pide el nombre del usuario para una conversación más cercana."
            }
        ]
    return session["contexto"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chatear():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    contexto = obtener_contexto()
    contexto.append({"role": "user", "content": mensaje})

    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=contexto
    )

    respuesta_ia = respuesta.choices[0].message.content
    contexto.append({"role": "assistant", "content": respuesta_ia})
    session["contexto"] = contexto

    return jsonify({"respuesta": respuesta_ia})

if __name__ == "__main__":
    app.run(debug=True)