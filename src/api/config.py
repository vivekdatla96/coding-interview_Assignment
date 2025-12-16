import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "weather"),
    "user": os.getenv("DB_USER", "db_user"),
    "password": os.getenv("DB_PASSWORD", "Pass@mysql123"),
}
