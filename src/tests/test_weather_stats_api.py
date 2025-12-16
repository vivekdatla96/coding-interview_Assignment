def test_get_weather_stats_success(client):
    response = client.get("/api/weather/stats")
    assert response.status_code == 200


def test_weather_stats_response_schema(client):
    response = client.get("/api/weather/stats")
    data = response.get_json()

    assert "data" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data

    if data["data"]:
        record = data["data"][0]
        assert "station_id" in record
        assert "year" in record
        assert "avg_max_temp" in record
        assert "avg_min_temp" in record
        assert "total_precipitation" in record


def test_filter_stats_by_station_id(client):
    response = client.get("/api/weather/stats?station_id=USC00110072")
    data = response.get_json()

    for record in data["data"]:
        assert record["station_id"] == "USC00110072"


def test_filter_stats_by_year(client):
    response = client.get("/api/weather/stats?year=1990")
    data = response.get_json()

    for record in data["data"]:
        assert record["year"] == 1990


def test_stats_pagination(client):
    response = client.get("/api/weather/stats?page=1&limit=10")
    data = response.get_json()

    assert len(data["data"]) <= 10
