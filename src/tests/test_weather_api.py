def test_get_weather_success(client):
    response = client.get("/api/weather")
    assert response.status_code == 200


def test_weather_response_is_json(client):
    response = client.get("/api/weather")
    assert response.is_json


def test_weather_response_schema(client):
    response = client.get("/api/weather")
    data = response.get_json()

    assert "data" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data

    if data["data"]:
        record = data["data"][0]
        assert "station_id" in record
        assert "date" in record
        assert "max_temp" in record
        assert "min_temp" in record
        assert "precipitation" in record


def test_filter_by_station_id(client):
    response = client.get("/api/weather?station_id=USC00110072")
    data = response.get_json()

    for record in data["data"]:
        assert record["station_id"] == "USC00110072"


def test_filter_by_date_range(client):
    response = client.get(
        "/api/weather?start_date=1985-01-01&end_date=1985-12-31"
    )
    data = response.get_json()

    for record in data["data"]:
        assert "1985-01-01" <= record["date"] <= "1985-12-31"


def test_weather_default_pagination(client):
    response = client.get("/api/weather")
    data = response.get_json()

    assert len(data["data"]) <= 20


def test_weather_custom_pagination(client):
    response = client.get("/api/weather?page=2&limit=5")
    data = response.get_json()

    assert len(data["data"]) <= 5


def test_invalid_date_format(client):
    response = client.get("/api/weather?start_date=20250101")
    assert response.status_code == 400
