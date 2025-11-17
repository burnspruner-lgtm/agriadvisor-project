# wsgi.py
# This is the "World-Class" entry point for your production server.

import logging

# 1. Import the app and startup functions
from scheduler_gateway import app, init_components, start_background_threads

# 2. Run the startup logic
# This initializes the database, components, and starts the AI thread
# *before* the server starts accepting requests.
try:
    logging.info("--- WSGI: Initializing components... ---")
    init_components()
    logging.info("--- WSGI: Starting background threads... ---")
    start_background_threads()
    logging.info("--- WSGI: Startup complete. Handing over to Gunicorn. ---")
except Exception as e:
    logging.critical(f"--- WSGI: FATAL ERROR ON STARTUP: {e} ---")
    # This will cause the server to fail to start, which is good.
    # It will show this error in your Render logs.
    raise

# 3. The `app` object is now exported for Gunicorn to use.
# Gunicorn will automatically find the object named `app`.