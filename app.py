from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# ------------------------
# STORAGE (ชั่วคราว)
# ------------------------
tasks = []

# ------------------------
# LOGIN
# ------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if username == "admin" and password == "1234":
        token = create_access_token(identity=username)
        return jsonify({
            "status": "success",
            "access_token": token
        })

    return jsonify({"error": "Invalid credentials"}), 401


# ------------------------
# GET TASKS
# ------------------------
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    return jsonify({
        "status": "success",
        "data": tasks
    })


# ------------------------
# CREATE TASK
# ------------------------
@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    task_text = data.get("task")

    if not task_text:
        return jsonify({"error": "Task is required"}), 400

    task = {
        "id": len(tasks) + 1,
        "task": task_text
    }

    tasks.append(task)

    return jsonify({
        "status": "success",
        "message": "Task created",
        "data": task
    })


# ------------------------
# EXTERNAL API (INTEGRATION)
# ------------------------
@app.route('/external-tasks', methods=['GET'])
@jwt_required()
def external_tasks():
    try:
        # 🔹 เปลี่ยนตรงนี้เป็น API เพื่อนจริงได้
        url = "https://jsonplaceholder.typicode.com/todos"

        response = requests.get(url, timeout=5)

        # เช็ค status
        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "Failed to fetch external API"
            }), 500

        external_data = response.json()[:5]

        return jsonify({
            "status": "success",
            "data": {
                "my_tasks": tasks,
                "external_tasks": external_data
            }
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "status": "error",
            "message": "External API timeout"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ------------------------
# ERROR HANDLER (เสริมให้ดูโปร)
# ------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ------------------------
# RUN
# ------------------------
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)