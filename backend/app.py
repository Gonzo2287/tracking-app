from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")

@app.route('/tracking/<numero>')
def tracking(numero):
    # Paso 1: detectar el courier automáticamente
    detect_url = "https://api.trackingmore.com/v4/couriers/detect"
    headers = {
        "Tracking-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    detect_body = { "tracking_number": numero }
    detect_response = requests.post(detect_url, headers=headers, json=detect_body)
    detect_data = detect_response.json()

    # Paso 2: elegir el primer courier detectado
    courier_code = "auto"
    if detect_data.get("data") and len(detect_data["data"]) > 0:
        courier_code = detect_data["data"][0]["courier_code"]

    # Paso 3: consultar el tracking
    track_url = "https://api.trackingmore.com/v4/trackings"
    track_body = {
        "tracking_number": numero,
        "courier_code": courier_code
    }
    track_response = requests.post(track_url, headers=headers, json=track_body)
    result = track_response.json()
    result["courier_detectado"] = courier_code
    return jsonify(result)

@app.route('/')
def inicio():
    return 'Servidor de tracking funcionando'

if __name__ == '__main__':
    app.run(debug=True)