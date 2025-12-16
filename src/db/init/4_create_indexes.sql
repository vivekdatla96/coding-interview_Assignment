USE weather;

CREATE INDEX idx_weather_station
    ON weather_observations (station_id);

CREATE INDEX idx_weather_date
    ON weather_observations (observation_date);
