CREATE TABLE weather_yearly_stats (
    station_id        VARCHAR(20) NOT NULL,
    year              INT NOT NULL,
    avg_max_temp_c    FLOAT NULL,
    avg_min_temp_c    FLOAT NULL,
    total_precip_cm   FLOAT NULL,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (station_id, year)
);
