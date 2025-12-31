import os
import edge_tts
import tempfile
import asyncio

from flask import Flask, jsonify, request, send_file
from ollama import Client
from config import gerar_system_prompt

app = Flask(__name__)

ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
client = Client(host=ollama_host)

dados = request.json
tema_solicitado = dados.get("theme", "F") 
lingua = dados.get("conversation_language", "EN")

system_content = gerar_system_prompt(lingua, tema_solicitado)

messages = [
    {"role": "system", "content": system_content},
]


@app.route("/")
def read_root():
    return jsonify({"message": "AILA AI Controller is running."})

@app.route("/status")
def check_status():
    try:
        models_response = client.list()

        if isinstance(models_response, dict):
            available_models = models_response.get('models', [])
        else:
            available_models = models_response.model_dump().get('models', [])

        return jsonify({"status": "online", "available_models": available_models})
    except Exception as e:
        return jsonify({"status": "offline", "error": str(e)}), 500
   
@app.route("/chat_audio", methods=["POST"])
def chat_audio():
    try:
        data = request.get_json()
        user_message = data.get("text")

        if not user_message:
            return jsonify({"error": "No message provided."}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload."}), 400

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat(
            model='gemma3:4b', 
            messages=messages, 
            stream=False)

        assistant_content = response['message']['content']

        messages.append({"role": "assistant", "content": assistant_content})

        audio_file_path = asyncio.run(generate_audio_file(assistant_content))

        return send_file(audio_file_path, mimetype="audio/mpeg")

    except Exception as e:
        if len(messages) > 1:
            messages.pop()
        
        return jsonify({"error": "Falha na comunicação com o modelo de IA: " + str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("text")

        if not user_message:
            return jsonify({"error": "No message provided."}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON payload."}), 400

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat(
            model='gemma3:4b', 
            messages=messages, 
            stream=False)

        assistant_content = response['message']['content']

        messages.append({"role": "assistant", "content": assistant_content})
        return jsonify({"response": assistant_content})

    except Exception as e:
        if len(messages) > 1:
            messages.pop()
        
        return jsonify({"error": "Falha na comunicação com o modelo de IA: " + str(e)}), 500

@app.route("/speak", methods=["POST"])
def speak():
    try:
        data = request.get_json()
        text_to_speak = data.get("text")

        if not text_to_speak:
            return jsonify({"error": "Nenhum texto foi fornecido."}), 400
    
        audio_file_path = asyncio.run(generate_audio_file(text_to_speak))

        return send_file(audio_file_path, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": "Falha na geração do áudio: " + str(e)}), 500

async def generate_audio_file(text, voice="pt-BR-ThalitaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    await communicate.save(temp_file.name)
    return temp_file.name

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)