from flask import Flask, request
import requests

app = Flask(__name__)
clients = []

@app.route("/")
def index():
    return "Siren Broadcast Server is Running"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    url = data.get("url")
    if url and url not in clients:
        clients.append(url)
        return f"등록됨: {url}"
    return "URL 누락됨", 400

@app.route("/broadcast", methods=["POST"])
def broadcast():
    data = request.get_json()
    message = data.get("message")
    for client in clients:
        try:
            requests.post(client, json={"message": message}, timeout=2)
        except Exception as e:
            print(f"❌ 전송 실패 → {client}: {e}")
    return "전송 완료"
