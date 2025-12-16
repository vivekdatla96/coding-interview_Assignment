import logging
from datetime import datetime
import mysql.connector
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("weather-aggregation")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "weather"),
    "user": os.getenv("DB_USER", "db_user"),
    "password": os.getenv("DB_PASSWORD","Pass@mysql123"),
}


AGGREGATION_SQL = """
INSERT INTO weather_yearly_stats (
    station_id,
    year,
    avg_max_temp_c,
    avg_min_temp_c,
    total_precip_cm
)
SELECT
    station_id,
    YEAR(observation_date) AS year,
    ROUND(AVG(max_temp) / 10, 2),
    ROUND(AVG(min_temp) / 10, 2),
    ROUND(SUM(precipitation) / 100, 2)
FROM weather_observations
GROUP BY station_id, YEAR(observation_date)
ON DUPLICATE KEY UPDATE
    avg_max_temp_c  = VALUES(avg_max_temp_c),
    avg_min_temp_c  = VALUES(avg_min_temp_c),
    total_precip_cm = VALUES(total_precip_cm);
"""


def main():
    start_time = datetime.utcnow()
    logger.info("Yearly weather aggregation started")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute(AGGREGATION_SQL)
        affected_rows = cursor.rowcount
        conn.commit()

        logger.info("Aggregation completed successfully")
        logger.info("Rows inserted/updated: %s", affected_rows)

    except Exception:
        conn.rollback()
        logger.exception("Aggregation failed")
        raise
    finally:
        cursor.close()
        conn.close()

    logger.info("Start time (UTC): %s", start_time)
    logger.info("End time (UTC): %s", datetime.utcnow())


if __name__ == "__main__":
    main()
