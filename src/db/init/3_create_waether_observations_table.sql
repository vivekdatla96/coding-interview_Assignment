USE weather;

CREATE TABLE IF NOT EXISTS weather_observations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    station_id VARCHAR(20) NOT NULL,
    observation_date DATE NOT NULL,
    max_temp INT NULL,
    min_temp INT NULL,
    precipitation INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_station
        FOREIGN KEY (station_id) REFERENCES stations(station_id),

    CONSTRAINT uq_station_date
        UNIQUE (station_id, observation_date)
);
