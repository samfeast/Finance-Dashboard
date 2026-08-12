from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ENV_PATH = PROJECT_ROOT / ".env"

DATABASE_PATH = PROJECT_ROOT / "data" / "data.db"

DATABASE_SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"

LOG_FILE = PROJECT_ROOT / "logs" / "finance-backend.log"

AUTH_REDIRECT_URI = "https://console.truelayer.com/redirect-page"
