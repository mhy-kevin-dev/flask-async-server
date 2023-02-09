
from flask import Flask, jsonify, request
import time
import uuid
import threading
import os
import json

app = Flask(__name__)


def process_request(request_data, id):
    # 模擬長時間的處理
    with app.app_context():
        print("--"*10, "running", "--"*10)
        print(f"-> GET ID: {id} ")
        res = jsonify({"message": "request done", "id": f"{id}", "results": "YAY"})
        time.sleep(10)
        with open(f"{id}.json", "w", encoding="utf-8") as f:
             json.dump(res.get_json(), f, indent=4)
        return res

@app.route("/get_report", methods=["POST"])
def get_report():
    print("--"*10, "get", "--"*10)
    data = request.get_json()
    id = data["id"]
    print(f"-> GET ID: {id} ")
    res = json.load(open(f"{id}.json", "r", encoding="utf-8"))
    return res

@app.route('/search', methods=['POST'])
def process():
    print("--"*10, "search", "--"*10)
    result = None
    data = request.get_json()
    id = str(uuid.uuid4())
    # Respond with processing message
    res = jsonify({'message': 'Processing...', 'id':f"{id}"})
    with open(f"{id}.json", "w", encoding="utf-8") as f:
         json.dump(res.get_json(), f, indent=4)
    # Start a new thread to do the processing
    thread = threading.Thread(target=process_request, args=(data, id))
    thread.start()
    return res

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=7733, debug=True) 



