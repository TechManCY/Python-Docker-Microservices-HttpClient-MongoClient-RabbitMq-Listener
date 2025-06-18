from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Dockerized Python App!"

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    name = data.get("name", "Guest")
    message = f"Hello, {name}! This is from Dockerized Python."
    return jsonify({"message": message, "status": "success"})

#http://localhost:5000/call-java
@app.route('/call-java')
def call_java():
    try:
        response = requests.get("http://host.docker.internal:8080/api/data") #host.docker.internal= app running on Windows (host machine)
        return jsonify({
            "from_java": response.json(),
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failure"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #http://localhost:5000/
    # run with : docker-compose run --rm app python main.py
    # update with :  docker-compose up --build app