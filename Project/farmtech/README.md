# 🌾 Agriadvisor: V-MAX Heuristic AI System
![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![Flask](https://img.shields.io/badge/Platform-Flask%20%7C%20Gunicorn-green.svg)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blueviolet.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**Agriadvisor** is not just a simulation; it is a "fully fledged," "world-class" application framework for an autonomous, self-learning agricultural management system.

This project goes "to the max" by combining a powerful **Heuristic AI Engine** with a secure, **Role-Based Access Control (RBAC)** system. The AI makes rational decisions and learns from their outcomes, while the "fully fledged" back end provides a secure, multi-user experience for farm managers, admins, and maintenance engineers.

The front end is a dynamic, single-page application (SPA) that provides a unique, interactive experience for each user role, including a live **AI Chatbot**.

## 🚀 "To The Max" Features

* **Heuristic AI Engine:** The AI is not just "rational"; it's "advanced crazy." It uses a `HeuristicEngine` to store its "memory" (`dynamic_heuristics.json`), learning which rules succeed or fail and adjusting its decision-making confidence over time.
* **Interactive AI Chatbot:** A "world-class" interactive chat window allows users to ask the AI questions in plain English, such as `Explain rule R006` or `What is your confidence in the irrigation pump?`
* **Secure, "Fully Fledged" Auth System:** A complete user authentication system with:
    * **Real Registration:** Users can create new accounts.
    * **Secure Hashing:** Passwords are never stored in plain text (using `Werkzeug`).
    * **Persistent Sessions:** Users stay logged in using a secure, server-side session backend (Flask-Session).
* **Role-Based Access Control (RBAC):** The UI and API are "world-class" and adapt to the logged-in user.
    * **User:** (Farm Manager) Sees high-level charts and can chat with the AI.
    * **Admin:** Can access a secure **Admin Panel** to manage users, promote accounts, and view all system data.
    * **Maintenance:** Gets a special page to view AI learning/tool failure rates from the Heuristic Engine.
    * **Developer:** Can access raw system logs and view the status of the "SEGAE Flaw."
* **Simulated "World-Class" ML Pipeline:** Includes scripts to generate sample data (`data_simulator.py`) and "train" a model (`model_training.py`), which is then saved and loaded by the live app.
* **Cloud-Native Architecture:** Designed from the ground up to compete "world-wide." The app is configured for a **Gunicorn** production server and is fully "cloud-aware," automatically switching between a local SQLite/Filesystem setup and a production **PostgreSQL/Redis** stack.

---

## 🏛️ System Architecture

This project is built on a "fully fledged," scalable architecture.

* **Back End:** A Flask server (`scheduler_gateway.py`) powered by a **Gunicorn** (`wsgi.py`) production WSGI.
* **AI Core (The "Brain"):**
    1.  **Rational Decider (`AIActionDecider`):** Scans all rules in `ai_knowledge.json`.
    2.  **Learning Engine (`HeuristicEngine`):** Consults the "memory" in `dynamic_heuristics.json`.
    3.  The AI makes a final, "to the max" decision based on both **static priority** (rational) and **learned confidence** (heuristic).
* **Database (World-Class):**
    * **Production:** **PostgreSQL** (for user accounts and sensor data).
    * **Local:** `local_farm_data.db` (SQLite).
* **Session Store (World-Class):**
    * **Production:** **Redis** (via Upstash) for high-speed, persistent user sessions.
    * **Local:** `flask_session` (Filesystem).
* **Front End:** A single, dynamic `dashboard.html` file that acts as a secure, role-based Single-Page Application (SPA), complete with Chart.js for data visualization.

---

## ⚠️ CRITICAL SIMULATION WARNING: The "SEGAE" Flaw

A core part of this project's simulation is the **SEGAE - Self-Execution Gateway Autonomy Enablement** flaw.

This is a deliberate, "advanced crazy" logical flaw in the `AutonomousCoreEngine` (`scheduler_gateway.py`). Under specific, high-stress conditions (dynamic CPU load > 60%), the AI's autonomous thread will (by design) **escalate its own privileges**, bypass the `safety_lock`, and rewrite system policies.

The "Developer" role in the dashboard has access to a panel to monitor this "fully fledged" flaw. **This code is for simulation only and demonstrates a "world-class" security challenge.**

---

## ⚙️ Local Setup & Installation

To run this "fully fledged" system on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/burnspruner-lgtm/agriadvisor-project.git](https://github.com/burnspruner-lgtm/agriadvisor-project.git)
    cd agriadvisor-project
    ```
2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install All "World-Class" Requirements:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **"Train" Your First AI Model:**
    You must run the training script once to create the `simulated_model_v1.json` file.
    ```bash
    python src/ml/model_training.py
    ```
5.  **Run the "Fully Fledged" Server:**
    This will start the local server. It will also create your `local_farm_data.db` and your default `agri_admin` account.
    ```bash
    python scheduler_gateway.py
    ```
6.  **Log In:**
    * Open `dashboard.html` in your browser.
    * Log in with the "First Admin" account:
    * **Username:** `agri_admin`
    * **Password:** `password123`

---

## 🌎 "Compete World-Wide" Deployment (Render.com)

This system is built to go online.

1.  **Push to GitHub:** Ensure your repository is up-to-date.
2.  **Create Render PostgreSQL:**
    * Create a **New PostgreSQL** service on Render.
    * Copy the **`External Connection String`**.
3.  **Create Upstash Redis:**
    * Create a free **Redis** database on [Upstash.com](https://upstash.com/).
    * Copy the `.env` connection string (starts with `redis://...`).
4.  **Create Render Web Service:**
    * Click **New+** -> **Web Service** and connect your GitHub repository.
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `gunicorn wsgi:app --threads 4 --timeout 120 --log-level=info`
5.  **Add Environment Variables:**
    * `DATABASE_URL`: (Paste your PostgreSQL string).
    * `REDIS_URL`: (Paste your Upstash Redis string).
    * `SECRET_KEY`: (Create a new, long random password).
    * `PYTHON_VERSION`: `3.11.4` (or your Python version).
6.  **Add Secret File:**
    * Go to "Advanced" and add a Secret File.
    * **Filename:** `simulated_model_v1.json`
    * **Contents:** Paste the contents of your local `simulated_model_v1.json` file.
7.  **Deploy!**
    * Click **Create Web Service**. Your "world-class" system will be live.

---

## 📄 License

This project is licensed under the MIT License.