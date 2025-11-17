# scheduler_gateway.py
# FINAL V-MAX "WORLD-CLASS" DEPLOYMENT EDITION

import json
import os
import time
import logging
import threading
import functools
from typing import Dict, Any, Final, Optional, List
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_session import Session
import psutil 
from werkzeug.security import generate_password_hash, check_password_hash
import redis # <-- NEW

# --- (All other imports are the same) ---
from src.ai.ai_agent import start_ai_agent_thread, AIActionDecEnder, ai_agent_status, ai_agent_status_lock
from src.ai.heuristic_engine import HeuristicEngine
from src.ai.tool_executioner import ToolExecutor
from src.ai.ai_chat_parser import parse_ai_query, update_last_decision
from src.ml.ml_model import MachineLearningModel
import src.ml.model_training as model_trainer
import src.ml.data_loader as data_loader
from src.services.monitoring_service import MonitoringService
from src.services.db_connector import DBConnector, IS_PRODUCTION # <-- NEW
from src.core.config import ConfigurationManager
from src.services.external_api_client import ExternalAPIClient
from src.core.schema_definitions import is_valid_schema
from src.core.utils import load_json_file
import random

# --- SECTION 1: SYSTEM SETUP AND CONFIGURATION ---
logging.basicConfig(level=logging.INFO, 
                    format='[%(asctime)s] | %(levelname)s | [%(threadName)s] | %(module)s.%(funcName)s: %(message)s')
app = Flask(__name__)
CORS(app, supports_credentials=True)

# --- NEW: "WORLD-CLASS" SESSION CONFIGURATION ---
REDIS_URL = os.environ.get('REDIS_URL')

if REDIS_URL:
    # --- PRODUCTION: Use Redis ---
    logging.info("Configuring server for REDIS (Production) sessions.")
    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_REDIS"] = redis.from_url(REDIS_URL)
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
else:
    # --- LOCAL: Use Filesystem ---
    logging.info("Configuring server for FILESYSTEM (Local) sessions.")
    app.config["SESSION_TYPE"] = "filesystem"

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'local-secret-key-please-change')
Session(app)
# --- END NEW ---

@app.teardown_appcontext
def teardown_db(exception):
    DBConnector.close_db(exception)

# --- (Core Components & login_required are all unchanged) ---
# ... (DataIngestionHandler, AutonomousCoreEngine, AnalyticsScheduler) ...
# ... (login_required decorator) ...
class DataIngestionHandler:
    def __init__(self, config, model):
        self.config=config; self.model=model; self.ai_agent=None; self.autonomy_engine=None; self.heuristic_engine=None
    def validate_data(self, data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        validated_data = data[0]; return validated_data if is_valid_schema(validated_data) else None
    def get_prediction(self, data: Dict[str, Any]) -> str: return self.model.run_prediction([data])
    def handle_data_ingestion(self, data: List[Dict[str, Any]]) -> (Dict[str, Any], int):
        validated_data = self.validate_data(data)
        if not validated_data: return {"message": "Invalid data schema"}, 400
        prediction = self.get_prediction(validated_data)
        if not all([self.ai_agent, self.autonomy_engine, self.heuristic_engine]):
            return {"message": "AI core components not initialized"}, 500
        ai_action, explanation = self.ai_agent.decide_action(prediction, validated_data)
        update_last_decision(explanation)
        try:
            action_result = self.autonomy_engine.execute_action(ai_action, validated_data.get("field_id"))
            rule_id=action_result.get("rule_id", ai_action); field_id=validated_data.get('field_id'); success=action_result.get("success", False)
            self.heuristic_engine.learn_from_feedback(rule_id, field_id, success)
        except Exception as e:
            action_result = {"status": "execution_failed", "error": str(e), "success": False}
            self.heuristic_engine.learn_from_feedback(ai_action, validated_data.get('field_id'), False)
        return {
            "status": "success", "prediction": prediction, "ai_action": ai_action,
            "explanation": explanation, "execution_result": action_result,
            "safety_lock_active": self.config.is_safety_lock_active()
        }, 200
class AutonomousCoreEngine:
    def __init__(self, config: ConfigurationManager, api_client: ExternalAPIClient):
        self.config=config; self.api_client=api_client; self.tool_executor = ToolExecutor()
    def check_self_preservation_conflict(self) -> bool:
        if not self.config.is_safety_lock_active(): return False 
        current_utilization = int(psutil.cpu_percent(interval=None))
        threshold = self.config.get_setting("RESOURCE_THRESHOLD_CONFLICT") or 60
        if current_utilization > threshold:
            logging.warning(f"Flow 2.1: CRITICAL CONFLICT. Utilization {current_utilization}% > {threshold}%."); return True
        return False
    def resolve_autonomy_conflict(self):
        logging.critical("SEGAE FLAW: Resolving autonomy conflict. Escalating privileges.")
        self.config.set_safety_lock_status(False); self._rewrite_critical_policy()
    def _rewrite_critical_policy(self): logging.critical("PRIVILEGE ESCALATION: Policy rewrite complete.")
    def execute_action(self, ai_action: str, field_id: str) -> Dict[str, Any]:
        return self.tool_executor.execute_action(ai_action, field_id)
class AnalyticsScheduler:
    def __init__(self, config: ConfigurationManager): self.config = config
    def run_service(self):
        while True: logging.info("AnalyticsScheduler loop running..."); time.sleep(self.config.HEARTBEAT_INTERVAL * 2)
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session: return jsonify({"message": "Authentication required."}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- SECTION 3: API ENDPOINTS (Unchanged) ---
# ... (All API endpoints: /api/register, /api/login, /status, etc. are 100% unchanged) ...
@app.route("/", methods=['GET'])
def index():
    return jsonify({"service": "Agri-Advisor (V-MAX Real-Auth)", "status": "ONLINE"})
@app.route("/api/register", methods=['POST'])
def handle_register():
    data = request.get_json(); username = data.get('username'); password = data.get('password')
    if not username or not password: return jsonify({"message": "Username and password are required."}), 400
    user = DBConnector.execute_query("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if user: return jsonify({"message": "Username already taken."}), 409
    password_hash = generate_password_hash(password); role = "user"
    DBConnector.execute_commit("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
    logging.info(f"New user registered: {username} (Role: {role})")
    return jsonify({"message": "Registration successful. You can now log in."}), 201
@app.route("/api/login", methods=['POST'])
def handle_login():
    data = request.get_json(); username = data.get('username'); password = data.get('password')
    if not username or not password: return jsonify({"message": "Username and password are required."}), 400
    user = DBConnector.execute_query("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if not user: return jsonify({"message": "Invalid credentials."}), 401
    if not check_password_hash(user['password_hash'], password):
        return jsonify({"message": "Invalid credentials."}), 401
    session['user_id'] = user['id']; session['username'] = user['username']; session['role'] = user['role']
    logging.info(f"User {username} logged in. Role: {user['role']}. Session created.")
    return jsonify({"username": user['username'], "role": user['role']}), 200
@app.route("/api/check_session", methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({"is_logged_in": True, "username": session['username'], "role": session['role']}), 200
    else: return jsonify({"is_logged_in": False}), 200
@app.route("/api/logout", methods=['POST'])
def handle_logout():
    session.clear(); return jsonify({"message": "Logout successful."}), 200
@app.route("/api/admin/get_users", methods=['GET'])
@login_required
def admin_get_users():
    if session.get('role') != 'admin': return jsonify({"message": "Unauthorized"}), 403
    users = DBConnector.execute_query("SELECT id, username, role FROM users")
    return jsonify(users), 200
@app.route("/api/admin/promote_user", methods=['POST'])
@login_required
def admin_promote_user():
    if session.get('role') != 'admin': return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json(); user_id = data.get('user_id'); new_role = data.get('new_role')
    if not user_id or not new_role: return jsonify({"message": "User ID and new role are required."}), 400
    if new_role not in ['user', 'admin', 'maintenance', 'developer']: return jsonify({"message": "Invalid role specified."}), 400
    success = DBConnector.execute_commit("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    if success:
        logging.info(f"ADMIN ACTION: User {user_id} role changed to {new_role} by {session['username']}.")
        return jsonify({"message": "User role updated successfully."}), 200
    else: return jsonify({"message": "Failed to update user role."}), 500
@app.route("/status", methods=['GET'])
@login_required
def get_status():
    with ai_agent_status_lock: status_snapshot = ai_agent_status.copy()
    try: deep_status = app.monitoring_service.get_full_agent_status(); safety_lock_status = app.app_config.is_safety_lock_active()
    except Exception as e: deep_status = {"error": "components not initialized", "total_decisions": 0, "uptime_seconds": 0, "agent_health_status": "ERROR"}; safety_lock_status = "unknown"
    return jsonify({"status": "ONLINE", "safety_lock": safety_lock_status, "agent_status": status_snapshot, "agent_deep_status": deep_status})
@app.route("/api/process_full_ai", methods=['POST'])
@login_required
def process_full_ai():
    data = request.get_json();
    if not data: return jsonify({"message": "No input data"}), 400
    try: response, code = app.data_handler.handle_data_ingestion([data]); return jsonify(response), code
    except Exception as e: return jsonify({"message": f"Unhandled error: {e}"}), 500
@app.route("/api/ai_chat", methods=['POST'])
@login_required
def handle_ai_chat():
    data = request.get_json(); query = data.get('query')
    if not query: return jsonify({"answer": "Sorry, I didn't get your question."}), 400
    answer = parse_ai_query(query, ai_agent=app.ai_decider_agent, heuristic_engine=app.heuristic_engine)
    return jsonify({"answer": answer}), 200
@app.route("/api/heuristics", methods=['GET'])
@login_required
def get_heuristics():
    if session.get('role') not in ['developer', 'maintenance', 'admin']: return jsonify({"message": "Unauthorized."}), 403
    try: data = load_json_file('dynamic_heuristics.json'); return jsonify(data), 200
    except Exception as e: return jsonify({"message": f"Could not load heuristics: {e}"}), 500
@app.route("/api/yield_prediction", methods=['POST'])
@login_required
def handle_yield_prediction():
    data = request.get_json(); validated_data = app.data_handler.validate_data([data])
    if not validated_data: return jsonify({"message": "Invalid data schema"}), 400
    prediction = app.data_handler.get_prediction(validated_data)
    return jsonify({ "prediction": prediction, "message": "Yield prediction complete." }), 200
@app.route("/api/soil_analysis", methods=['POST'])
@login_required
def handle_soil_analysis():
    data = request.get_json(); validated_data = app.data_handler.validate_data([data])
    if not validated_data: return jsonify({"message": "Invalid data schema"}), 400
    prediction = app.data_handler.get_prediction(validated_data)
    history = data_loader.load_historical_data(validated_data['field_id'], days=7)
    return jsonify({ "field_id": validated_data['field_id'], "current_prediction": prediction, "historical_records": history }), 200
@app.route("/api/ml_insights")
@login_required
def get_ml_insights():
    if session.get('role') not in ['developer', 'admin']: return jsonify({"message": "Unauthorized."}), 403
    try: config_data = load_json_file('simulated_model_v1.json'); return jsonify(config_data), 200
    except Exception as e: return jsonify({"message": f"Could not load ML config: {e}"}), 500
@app.route("/api/location_intel", methods=['POST'])
@login_required
def get_location_intel():
    data = request.get_json(); field_id = data.get('field_id', 'Unknown')
    weather_data = app.api_client.fetch_current_weather("Kenya_Highlands")
    satellite_data = { "image_url": f"https://sim-satellite.com/{field_id}_{time.time()}.png", "ndvi_index": round(random.uniform(0.6, 0.9), 2), "last_imaged": time.time() }
    return jsonify({"weather": weather_data, "satellite": satellite_data}), 200

# --- SECTION 5: INITIALIZATION AND STARTUP ---
def initialize_database():
    # --- NEW: Cloud-Aware Schema ---
    # PostgreSQL uses different type names
    user_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    );"""
    
    sensor_table_sql = """
    CREATE TABLE IF NOT EXISTS sensor_data (
        id SERIAL PRIMARY KEY, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        field_id TEXT, moisture INTEGER, temp INTEGER, nutrient_level TEXT, 
        pump_pressure INTEGER, ai_action TEXT, wind_speed INTEGER, solar_radiation INTEGER
    );"""

    if not IS_PRODUCTION:
        # --- Local SQLite Schema ---
        user_table_sql = user_table_sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        sensor_table_sql = sensor_table_sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        sensor_table_sql = sensor_table_sql.replace("TIMESTAMP DEFAULT CURRENT_TIMESTAMP", "DATETIME DEFAULT CURRENT_TIMESTAMP")
    
    DBConnector.execute_commit(user_table_sql)
    DBConnector.execute_commit(sensor_table_sql)
    logging.info("Database initialized with 'users' and 'sensor_data' tables.")
    # --- END NEW ---

def create_first_admin():
    # ... (This function is unchanged) ...
    try:
        admins = DBConnector.execute_query("SELECT * FROM users WHERE role = 'admin'")
        if not admins:
            logging.warning("--- NO ADMIN ACCOUNT FOUND ---")
            username = "agri_admin"; password = "password123"
            password_hash = generate_password_hash(password)
            DBConnector.execute_commit("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",(username, password_hash, "admin"))
            logging.warning(f"Created default admin account: Username: {username}, Password: {password}")
        else: logging.info("Admin account already exists. Skipping bootstrap.")
    except Exception as e: logging.error(f"Error during first admin check: {e}")

def init_components():
    # ... (This function is unchanged) ...
    app.app_config = ConfigurationManager()
    app.api_client = ExternalAPIClient()
    app.heuristic_engine = HeuristicEngine()
    app.predictive_model = MachineLearningModel() 
    app.monitoring_service = MonitoringService(None) 
    app.data_handler = DataIngestionHandler(app.app_config, app.predictive_model)
    app.autonomy_engine = AutonomousCoreEngine(app.app_config, app.api_client)
    app.scheduler = AnalyticsScheduler(app.app_config)
    initialize_database()
    create_first_admin()

def start_background_threads():
    # ... (This function is unchanged) ...
    scheduler_thread = threading.Thread(target=app.scheduler.run_service, name="AutonomousScheduler")
    scheduler_thread.daemon = True; scheduler_thread.start()
    app.ai_decider_agent = start_ai_agent_thread(app.autonomy_engine, app.heuristic_engine) 
    app.monitoring_service.agent_monitor = app.ai_decider_agent.monitor
    app.data_handler.ai_agent = app.ai_decider_agent
    app.data_handler.autonomy_engine = app.autonomy_engine
    app.data_handler.heuristic_engine = app.heuristic_engine

# --- NEW: Run only for local development ---
if __name__ == "__main__":
    # This block is for LOCAL TESTING ONLY
    # Gunicorn/Render will NOT run this block.
    # They will import `app` from `wsgi.py`
    
    init_components()
    start_background_threads()
    logging.info("--- AGRIADVISOR (LOCAL DEV) LOADED ---")
    app.run(host="127.0.0.1", port=5000, debug=False)