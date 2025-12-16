import os
import logging
from datetime import datetime
import mysql.connector

# -----------------------
# Configuration
# -----------------------
WX_DATA_DIR = os.getenv("WX_DATA_DIR", "wx_data")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000)) 
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "weather"),
    "user": os.getenv("DB_USER", "db_user"),
    "password": os.getenv("DB_PASSWORD","Pass@mysql123"),
}

MISSING_VALUES = {"-9999", "-", ""}

# -----------------------
# Logging
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("weather-ingestion")

# -----------------------
# Helpers
# -----------------------
def parse_int(value: str):
    value = value.strip()
    if value in MISSING_VALUES:
        return None
    return int(value)


def parse_weather_line(line: str):
    """
    Expected format (whitespace delimited):
    YYYYMMDD max_temp min_temp precipitation
    """
    parts = line.strip().split()

    if len(parts) != 4:
        raise ValueError(f"Invalid record format: {line}")

    return (
        datetime.strptime(parts[0], "%Y%m%d").date(),
        parse_int(parts[1]),
        parse_int(parts[2]),
        parse_int(parts[3]),
    )


# -----------------------
# Database Operations
# -----------------------
def get_connection():
    return mysql.connector.connect(**DB_CONFIG, autocommit=False)


def upsert_station(cursor, station_id):
    cursor.execute(
        """
        INSERT IGNORE INTO stations (station_id, state)
        VALUES (%s, %s)
        """,
        (station_id, station_id[:2]),
    )


def insert_weather_batch(cursor, rows):
    sql = """
        INSERT INTO weather_observations
        (station_id, observation_date, max_temp, min_temp, precipitation)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            max_temp = VALUES(max_temp),
            min_temp = VALUES(min_temp),
            precipitation = VALUES(precipitation)
    """
    cursor.executemany(sql, rows)


# -----------------------
# Main Ingestion Logic
# -----------------------
def ingest_weather_data():
    start_time = datetime.utcnow()
    logger.info("Weather ingestion started")

    total_records_read = 0
    total_records_written = 0

    conn = get_connection()
    cursor = conn.cursor()

    try:
        for file_name in sorted(os.listdir(WX_DATA_DIR)):
            if not file_name.endswith(".txt"):
                continue

            station_id = file_name.replace(".txt", "")
            file_path = os.path.join(WX_DATA_DIR, file_name)

            logger.info("Processing station %s", station_id)
            upsert_station(cursor, station_id)

            batch = []

            with open(file_path, "r") as f:
                for line in f:
                    total_records_read += 1
                    try:
                        obs_date, max_t, min_t, precip = parse_weather_line(line)
                    except Exception as e:
                        logger.warning("Skipping bad record: %s | %s", line.strip(), e)
                        continue

                    batch.append(
                        (station_id, obs_date, max_t, min_t, precip)
                    )

                    if len(batch) >= BATCH_SIZE:
                        insert_weather_batch(cursor, batch)
                        conn.commit()
                        total_records_written += len(batch)
                        batch.clear()

                if batch:
                    insert_weather_batch(cursor, batch)
                    conn.commit()
                    total_records_written += len(batch)

        end_time = datetime.utcnow()
        logger.info("Weather ingestion completed")
        logger.info("Start time (UTC): %s", start_time)
        logger.info("End time (UTC): %s", end_time)
        logger.info("Total records read: %d", total_records_read)
        logger.info("Total records written/updated: %d", total_records_written)

    except Exception:
        conn.rollback()
        logger.exception("Weather ingestion failed")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    ingest_weather_data()