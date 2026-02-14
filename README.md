

## 📌 Project Overview

**FixNow** is a web-based service booking platform developed using **Flask** and **SQLite**. The application connects users with skilled workers such as electricians, plumbers, and technicians. Users can register, log in, book services, and provide feedback. Workers can register, manage their profile, and view their ratings and performance score.

The system ensures smooth interaction between users and workers through secure authentication and structured database management.

---

## 🎯 Problem Statement

Finding reliable local service workers is often difficult and time-consuming. There is no centralized system to book services, track performance, and collect feedback. FixNow solves this problem by providing a digital platform where users can easily find workers, book services, and rate them, while workers can showcase their services and performance.

---

## 🧰 Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS
* **Database:** SQLite3
* **Template Engine:** Jinja2
* **Authentication:** Flask Sessions

---

## ✨ Features

* User Registration & Login
* Worker Registration
* Worker Dashboard with Rating & Performance Score
* Service Booking System
* Feedback & Review System
* Session-Based Authentication
* SQLite Database Integration

---

## 📂 Project Structure

```
fixnow/
│
├── app.py
├── database.db
└── templates/
    ├── home.html
    ├── user_register.html
    ├── user_login.html
    ├── worker_register.html
    ├── dashboard.html
    ├── worker_dashboard.html
    ├── booking.html
    └── feedback.html
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone <your-repository-link>
```

2. Navigate to project directory:

```bash
cd fixnow
```

3. Install dependencies:

```bash
pip install flask
```

(SQLite is built into Python, so no separate installation is required.)

---

## ▶️ Running the Application

```bash
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000/
```

---

## 🏗 Architecture

```
User/Worker (Browser)
        ↓
     Flask Application (app.py)
        ↓
     SQLite Database
  (Users, Workers, Bookings, Feedback)
```

---

## 📘 API Routes

### User Routes

* `GET /` – Home Page
* `GET/POST /user_register` – Register User
* `GET/POST /user_login` – Login User
* `GET /dashboard` – User Dashboard

### Worker Routes

* `GET/POST /worker_register` – Register Worker
* `GET /worker_dashboard/<worker_id>` – Worker Dashboard

### Booking & Feedback

* `GET/POST /book/<worker_id>` – Book Worker
* `GET /payment_success/<worker_id>` – Payment Redirect
* `GET/POST /feedback/<worker_id>` – Submit Feedback

---

## 📸 Screenshots

(Add screenshots here)

* Home Page
* User Dashboard
* Worker Dashboard
* Booking Page

---

## 🎥 Demo Video

(Add your demo video link here)

---

## 👩‍💻 Team Members

* Sreelakshmi S Nair
* fathimathul farsana

---

## 📜 License

This project is developed for academic and learning purposes.


