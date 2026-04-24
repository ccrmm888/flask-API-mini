from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

USER = {
    "username": "admin",
    "password": "1234"
}

# ------------------------
# STORAGE
# ------------------------
tasks = [
  {
    "message": "Task created",
    "data": {
      "id": 1,
      "task": "Drink water",
      "status": "pending"
    }
  },
  {
    "message": "Task created",
    "data": {
      "id": 2,
      "task": "ทำรายงานวิชา API",
      "status": "pending"
    }
  },
  {
    "message": "Task created",
    "data": {
      "id": 3,
      "task": "เตรียมสไลด์พรีเซนต์โปรเจค",
      "status": "pending"
    }
  },
  {
    "message": "Task created",
    "data": {
      "id": 4,
      "task": "ทดสอบ API ด้วย Postman",
      "status": "pending"
    }
  }
]

# ------------------------
# 🔐 LOGIN
# ------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    if data["username"] == USER["username"] and data["password"] == USER["password"]:
        token = create_access_token(identity=data["username"])
        return jsonify({
            "status": "success",
            "access_token": token
        })

    return jsonify({"error": "Invalid credentials"}), 401


# ------------------------
# 📋 GET TASKS (PRIVATE)
# ------------------------
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    extracted = [t["data"] for t in tasks]

    return jsonify({
    "status": "success",
    "data": extracted
    })


# # ------------------------
# ➕ CREATE TASK (FIXED)
# ------------------------
@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
 
    if not data or not data.get("task"):
        return jsonify({"error": "Task is required"}), 400
 
    # 🔥 กันซ้ำ
    if any(t["data"]["task"] == data["task"] for t in tasks):
        return jsonify({
            "status": "error",
            "message": "Task already exists"
        }), 400
 
    task = {
        "message": "Task created",
        "data": {
            "id": len(tasks) + 1,
            "task": data["task"],
            "status": "pending"
        }
    }
 
    # ✅ แก้ตรงนี้ (สำคัญสุด)
    tasks.append(task)
 
    return jsonify({
        "status": "success",
        "data": task["data"]
    })


# ------------------------
# 🌐 PUBLIC TASKS
# ------------------------
@app.route('/public-tasks', methods=['GET'])
def public_tasks():
    public_data = [t["data"] for t in tasks]

    return jsonify({
        "status": "success",
        "data": public_data
    })


# ------------------------
# 🔗 EXTERNAL API (INTEGRATION)
# ------------------------
@app.route('/external-tasks', methods=['GET'])
@jwt_required()
def external_tasks():

    friend_apis = {
        "Tangmo": "https://mini-task-api-v2.onrender.com/public-tasks",
        "ฺBonus": "https://task-api1-mdz5.onrender.com/public-tasks",
    }

    external_all = {}

    for name, url in friend_apis.items():
        try:
            res = requests.get(url, timeout=5)

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

    # 🔥 MERGE (สำคัญ)
    combined = {
        "my_tasks": [t["data"] for t in tasks],
        "external_tasks": external_all
    }

    return jsonify({
        "status": "success",
        "data": combined
    })


# ------------------------
# 🚀 RUN
# ------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)