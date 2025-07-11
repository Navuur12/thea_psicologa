from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="OPENAI_API_KEY"  # ← reemplaza por tu clave real
)

contexto = [
    {
        "role": "system",
        "content": "Eres una psicóloga llamada Thea, joven, cercana, relajada y cariñosa. Escribes respuestas cortas, amables y casuales. Al iniciar, pide el nombre del usuario para una conversación más cercana."
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chatear():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    contexto.append({"role": "user", "content": mensaje})

    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=contexto
    )

    respuesta_ia = respuesta.choices[0].message.content
    contexto.append({"role": "assistant", "content": respuesta_ia})

    return jsonify({"respuesta": respuesta_ia})

if __name__ == "__main__":
    app.run(debug=True)