from flask import Flask, request, jsonify
import jwt
import requests
import os
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysterykey888'
 
#user
USER = {
    "username": "mina",
    "password": "888888"
}
 
#database
tasks = [ { "message": "Task created", "data": { "id": 1, "task": "Drink water", "status": "pending" } }, { "message": "Task created", "data": { "id": 2, "task": "ทำรายงานวิชา API", "status": "pending" } }, { "message": "Task created", "data": { "id": 3, "task": "เตรียมสไลด์พรีเซนต์โปรเจค", "status": "pending" } }, { "message": "Task created", "data": { "id": 4, "task": "ทดสอบ API ด้วย Postman", "status": "pending" } } ]
 
#log in
@app.route('/login', methods=['POST'])
def login():
    data = request.json
 
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({
            "error": {
                "code": 400,
                "message": "Missing username or password"
            }
        }), 400
 
    if data["username"] == USER["username"] and data["password"] == USER["password"]:
        token = jwt.encode({
            "user": data["username"],
        }, app.config['SECRET_KEY'], algorithm="HS256")
 
        return jsonify({"token": token})
 
    return jsonify({
        "error": {
            "code": 401,
            "message": "Invalid credentials"
        }
    }), 401
 
 
#token verification
def verify_token(req):
    auth = req.headers.get("Authorization")
 
    if not auth:
        return None, ("Missing token", 401)
 
    try:
        token = auth.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return data, None
    except:
        return None, ("Invalid token", 401)
 
 
#get tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    user, error = verify_token(request)
    if error:
        return jsonify({"error": {"code": error[1], "message": error[0]}}), error[1]
 
    return jsonify({"tasks": tasks})
 
 
#create task
@app.route('/tasks', methods=['POST'])
def create_task():
    user, error = verify_token(request)
    if error:
        return jsonify({"error": {"code": error[1], "message": error[0]}}), error[1]

    data = request.json

    if not data or not data.get("task"):
        return jsonify({
            "error": {
                "code": 400,
                "message": "Task is required"
            }
        }), 400

    new_task = {
        "message": "Task created",
        "data": {
            "id": len(tasks) + 1,
            "task": data["task"],
            "status": data.get("status", "pending")
        }
    }

    tasks.append(new_task)

    return jsonify(new_task)
 
 
#public tasks
@app.route('/public-tasks', methods=['GET'])
def public_tasks():
    return jsonify({
        "tasks": [t["data"] for t in tasks]
    })
 
 
#external tasks
@app.route('/external-tasks', methods=['GET'])
def external_tasks():
    user, error = verify_token(request)
    if error:
        return jsonify({"error": {"code": error[1], "message": error[0]}}), error[1]
 
    friend_apis = {
        "Bonus": "https://task-api1-mdz5.onrender.com",
        "Cream": "https://flask-api-mini-1.onrender.com/public-tasks"
    }
 
    external_all = {}
 
    for name, url in friend_apis.items():
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if "tasks" in data:
                    external_all[name] = data["tasks"]
                elif "data" in data:
                    external_all[name] = data["data"]
                else:
                    external_all[name] = data
 
            else:
                external_all[name] = {"error": f"{url} returned {res.status_code}"}
        except:
            external_all[name] = {"error": f"Cannot connect to {url}"}
 
    return jsonify({
    "status": "success",
    "data": {
        "my_tasks": [t["data"] for t in tasks],
        "external_tasks": external_all
    }
})
 
@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": {
            "code": 500,
            "message": "Internal server error"
        }
    }), 500
 
#run run run away
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
 