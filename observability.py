import logging
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
# CLOUD FIX: Use /tmp for logs in production
if os.path.exists("/tmp"):
    LOG_DIR = "/tmp/logs"
else:
    LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

class JsonFormatter(logging.Formatter):
    """
    Formats log records as JSON objects for machine readability.
    This enables 'Structured Logging' - a key Enterprise requirement.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "component": record.name,
            "message": record.getMessage(),
            "file": record.filename,
            "line": record.lineno
        }
        return json.dumps(log_record)

def setup_observability():
    """
    Configures the Global Logger.
    Call this ONCE at the start of the application.
    """
    # 1. Get the Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear existing handlers (to avoid duplicates from basicConfig)
    if root_logger.handlers:
        root_logger.handlers.clear()

    # 2. Channel A: Console (Human Friendly)
    # Prints: [10:00:00] INFO | Manager | Message...
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # 3. Channel B: Audit File (Machine Friendly)
    # Saves: {"timestamp": "...", "component": "CFO", "message": "..."}
    # We use a new file for each session to keep things clean.
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(LOG_DIR, f"trace_{session_id}.jsonl")
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(file_handler)

    logging.info(f"🔭 Observability initialized. Audit trail: {log_file}")