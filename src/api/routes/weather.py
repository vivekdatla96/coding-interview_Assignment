from flask_restx import abort, Namespace, Resource, fields
from flask import request
from api.db import get_connection
from datetime import datetime

ns = Namespace("weather", description="Daily weather observations")

weather_record = ns.model(
    "Weather",
    {
        "station_id": fields.String,
        "date": fields.String,
        "max_temp": fields.Integer,
        "min_temp": fields.Integer,
        "precipitation": fields.Integer,
    },
)

weather_response = ns.model(
    "WeatherResponse",
    {
        "data": fields.List(fields.Nested(weather_record)),
        "page": fields.Integer,
        "limit": fields.Integer,
        "total": fields.Integer,
    },
)

def serialize_weather_rows(rows):
    """
    Convert date objects to ISO strings for JSON serialization.
    """
    for row in rows:
        if row.get("date"):
            row["date"] = row["date"].isoformat()
    return rows

def validate_date(date_str: str, field_name: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        abort(
            400,
            f"Invalid {field_name} format. Expected YYYY-MM-DD."
        )

@ns.route("")
class Weather(Resource):
    @ns.param('station_id', 'Weather station ID')
    @ns.param('start_date', 'Start date (YYYY-MM-DD)')
    @ns.param('end_date', 'End date (YYYY-MM-DD)')
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('limit', 'Records per page', type=int, default=20)
    #@ns.marshal_list_with(weather_model)

    def get(self):
        station_id = request.args.get("station_id")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if start_date:
            validate_date(start_date, "start_date")

        if end_date:
            validate_date(end_date, "end_date")

        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
        offset = (page - 1) * limit

        base_query = """
            FROM weather_observations
            WHERE 1=1
        """
        params = []

        if station_id:
            base_query += " AND station_id = %s"
            params.append(station_id)

        if start_date:
            base_query += " AND observation_date >= %s"
            params.append(start_date)

        if end_date:
            base_query += " AND observation_date <= %s"
            params.append(end_date)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        count_query = "SELECT COUNT(*) AS total " + base_query
        cursor.execute(count_query, params)
        total = cursor.fetchone()["total"]

        data_query = (
            "SELECT station_id, observation_date AS date, "
            "max_temp, min_temp, precipitation "
            + base_query +
            " ORDER BY observation_date "
            " LIMIT %s OFFSET %s"
        )

        data_params = params + [limit, offset]
        cursor.execute(data_query, data_params)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        rows = serialize_weather_rows(rows)

        return {
            "data": rows,
            "page": page,
            "limit": limit,
            "total": total
        }, 200
