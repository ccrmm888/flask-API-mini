# Task API Mini Project

ระบบ API ที่ทำด้วย Flask ใช้จัดการ Task มีระบบล็อกอินด้วย JWT และสามารถดึงข้อมูลจาก API ของเพื่อนได้

## 1. ภาพรวม (Overview)

โปรเจคนี้พัฒนาด้วย Python และ Flask

รองรับการทำงาน:

* เพิ่มรายการ Task
* ยืนยันตัวตนผู้ใช้งานด้วย JWT (Token)
* สามารถใช้งาน Public API ได้(ไม่ต้องใช้ Token)
* สามารถเชื่อมต่อกับ API ของเพื่อน (External Integration)

ระบบนี้แสดงให้เห็นถึง:

* การออกแบบ API
* โครงสร้าง Request/Response
* การทำ Authentication
* การจัดการ Error
* การเชื่อมต่อระหว่างระบบของตัวเรากับเพื่อนๆ (Integration)


## 2. ฟีเจอร์หลัก (Features)

* ระบบยืนยันตัวตนด้วย JWT
* ดูรายการ Task (ต้องใช้ Token)
* เพิ่ม Task
* ดู Task แบบ Public (ไม่ต้องใช้ Token)
* เชื่อมต่อ API ภายนอก
* รองรับ Error (400 / 401 / 500)


## 3. เทคโนโลยีที่ใช้ (Technology Stack)

* Python
* Flask
* PyJWT
* Requests
* JSON ผ่าน HTTP


## 4. วิธีใช้งาน (How to Run)

### 4.1 Clone โปรเจค

Command Prompt
git clone https://your-repo-url.git
cd project


### 4.2 สร้าง Virtual Environment

Command Prompt
เพื่อแยก dependency ของโปรเจค
python -m venv venv


### 4.3 เปิดใช้งาน Virtual Environment

Command Prompt
Windows:
venv\Scripts\activate

Mac / Linux:
source venv/bin/activate


### 4.4 ติดตั้ง Flask

Command Prompt
pip install flask


### 4.5 ไปหน้าโค้ด

Command Prompt
code .


### 4.6 ติดตั้ง Dependencies

Terminal
pip install flask flask-jwt-extended requests


### 4.7 รันเซิร์ฟเวอร์

python app.py


### 4.8 อัปโหลดขึ้น Github

git init
git code .
git commit -m "first commit"
git push

### 4.9 Deploy API

นำลิงค์ Github ไป Deploy ที่ Render.com


## 5. การยืนยันตัวตน (Authentication) ที่ postman

เรียกใช้งาน `/login` เพื่อรับ Token:
[POST] url/login


[POST] url/tasks
Authorization: Bearer <token>



## 6. API Endpoints

### Login

POST /login


### 📋 ดู Task (Private)

จากนั้นนำ Token ไปใส่ใน Header:
[GET] url/tasks
Authorization: Bearer <token>

### เพิ่ม Task

จากนั้นนำ Token ไปใส่ใน Header:
[GET] url/tasks
Authorization: Bearer <token>

[POST] url/tasks
Authorization: Bearer <token>

### Public Tasks

GET /public-tasks
ไม่ต้องใช้ Token

### External Tasks

GET /external-tasks
ต้องใช้ Token

---

## 7. ตัวอย่าง Request และ Response

### ✅ Login

```json
{
  "username": "mina",
  "password": "888888"
}
```

Response:

```json
{
  "token": "your_jwt_token"
}
```

---

### Login ไม่สำเร็จ

```json
{
  "error": {
    "code": 401,
    "message": "Invalid credentials"
  }
}
```

---

### ดู Task

```json
{
  "tasks": [
    {
      "message": "Task created",
      "data": {
        "id": 1,
        "task": "Drink water",
        "status": "pending"
      }
    }
  ]
}
```

---

### เพิ่ม Task

```json
{
  "task": "อ่านหนังสือสอบ"
}
```

Response:

```json
{
  "message": "Task created",
  "data": {
    "id": 5,
    "task": "อ่านหนังสือสอบ",
    "status": "pending"
  }
}
```

---

### Error (400)

```json
{
  "error": {
    "code": 400,
    "message": "Task is required"
  }
}
```

---

### Public Tasks

```json
{
  "tasks": [
    {
      "id": 1,
      "task": "Drink water",
      "status": "pending"
    }
  ]
}
```

---

### External Tasks

```json
{
  "status": "success",
  "data": {
    "Cream": [...],
    "external_tasks": {
      "Bonus": [...],
      "Tangmo": [...]
    }
  }
}
```

---

## 8. ขั้นตอนการทำงานของ Integration

1. เซิร์ฟเวอร์ส่ง request ไปยัง API ของเพื่อน
2. รอรับข้อมูล JSON
3. ตรวจสอบรูปแบบข้อมูล
4. รวมข้อมูล (merge)
5. ส่งผลลัพธ์กลับให้ผู้ใช้

---

## 9. HTTP Status Codes ที่ใช้

* 200 OK
* 201 Created
* 400 Bad Request
* 401 Unauthorized
* 404 Not Found
* 500 Internal Server Error

---

## 10. การจัดการ Error

ตัวอย่าง 500:

```json
{
  "error": {
    "code": 500,
    "message": "Internal server error"
  }
}
```


## 11. ความปลอดภัย (Security)

* ไม่ควรใส่ Secret Key ไว้ในโค้ด
* ใช้ Environment Variables
* ใช้ HTTPS


## 12. สิ่งที่สามารถพัฒนาต่อได้

* เพิ่มฐานข้อมูล (PostgreSQL)
* เพิ่ม API สำหรับแก้ไข / ลบ Task
* เพิ่ม Token Expiration (exp)


## 👤 ผู้จัดทำ

Pagamas Thongkratok
ผกามาศ ธงกระโทก
