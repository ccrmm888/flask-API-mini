from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests
import os

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
# PRIVATE TASKS (ต้องมี token)
# ------------------------
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    return jsonify({
        "status": "success",
        "data": tasks
    })


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
# PUBLIC TASKS (เพื่อนเรียกได้ ไม่ต้อง token)
# ------------------------
@app.route('/public-tasks', methods=['GET'])
def public_tasks():
    return jsonify({"tasks": tasks})


# ------------------------
# EXTERNAL API (ดึงของเพื่อนแบบไม่ใช้ token)
# ------------------------
@app.route('/external-tasks', methods=['GET'])
@jwt_required()
def external_tasks():
    try:
        # 🔥 เปลี่ยน URL นี้เป็นของเพื่อน
        url = "https://jsonplaceholder.typicode.com/todos"

        response = requests.get(url, timeout=5)

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
# OPTIONAL: PUBLIC EXTERNAL (ไม่ต้อง token)
# ------------------------
@app.route('/external-public', methods=['GET'])
def external_public():
    try:
        # 🔥 ใช้ public endpoint ของเพื่อน
        url = "https://mini-task-api-v2.onrender.com"

        response = requests.get(url, timeout=5)
        external_data = response.json()[:5]

        return jsonify({
            "status": "success",
            "data": external_data
        })

    except:
        return jsonify({"error": "External API failed"}), 500


# ------------------------
# ERROR HANDLER
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
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)