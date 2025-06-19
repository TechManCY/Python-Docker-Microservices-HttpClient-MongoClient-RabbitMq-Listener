from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

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

# Read windows mongoDB 
# http://localhost:5000/get-users
DB_NAME = "mongo_query_practice"
COLLECTION_NAME = "student_wrappers_extend"

MONGO_URI = "mongodb://host.docker.internal:27017/" # host.docker.internal allows Docker to access the host's localhost

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/get-users')
def get_users():
    try:
        users = list(collection.find({}, {'_id': 0}))  # exclude MongoDB's _id field
        return jsonify({"users": users, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "failure"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #http://localhost:5000/
    # run with : docker-compose run --rm app python main.py
    # update with :  docker-compose up --build app consumer