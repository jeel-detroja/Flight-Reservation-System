# ✈️ Flight Reservation System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

A full-stack web application that allows users to seamlessly search, view, and book flights in real-time using city-based inputs. Powered by the Amadeus API, this system provides accurate flight data, pricing, and a smooth multi-step booking experience.

---

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#️-how-to-run-step-by-step)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Features
- **Smart City Search:** Search for flights using natural city names instead of complex airport codes.
- **Live Flight Data:** Integration with the Amadeus Flight API for real-time routes, timings, and availability.
- **Comprehensive Details:** View airlines, departure/arrival times, and up-to-date pricing.
- **Multi-Step Booking:** A clean, guided booking system for a smooth user experience.
- **Interactive UI:** Responsive and intuitive frontend design.

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **API:** Amadeus Flight API
- **Database:** SQLite

---

## 🛑 Prerequisites
Before you begin, ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- An active developer account with [Amadeus for Developers](https://developers.amadeus.com/) to get your API keys.

---

## ⚙️ How to Run (Step-by-Step)

### 1️⃣ Clone the Repository
Open your terminal and clone the project to your local machine:
```bash
git clone [https://github.com/jeel-detroja/Flight-Reservation-System.git](https://github.com/jeel-detroja/Flight-Reservation-System.git)
cd Flight-Reservation-System
```

### 2️⃣ Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
```bash
python -m venv venv
```

### 3️⃣ Activate the Virtual Environment
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4️⃣ Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 5️⃣ Set Up Security (.gitignore)
Before creating your environment variables, ensure they won't be pushed to GitHub. Create a `.gitignore` file in your root directory and add the following:
```text
# Environments
venv/
env/

# Environment Variables
.env

# Database
db.sqlite3

# Python Caches
__pycache__/
*.pyc
```

### 6️⃣ Add API Credentials
Create a `.env` file in the root directory of your project and add your Amadeus API keys:
```env
AMADEUS_CLIENT_ID=your_api_key_here
AMADEUS_CLIENT_SECRET=your_secret_key_here
```

### 7️⃣ Run Migrations
Set up your SQLite database:
```bash
python manage.py migrate
```

### 8️⃣ Start the Server
Run the Django development server:
```bash
python manage.py runserver
```

### 9️⃣ Open in Browser
Navigate to the following URL in your web browser:
```text
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
```


---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 
Feel free to check the [issues page](https://github.com/jeel-detroja/Flight-Reservation-System/issues) if you want to contribute.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE). 

---
*Built by [jeel-detroja](https://github.com/jeel-detroja)*
