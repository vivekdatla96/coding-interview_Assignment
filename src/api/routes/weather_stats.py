from flask import request
from flask_restx import Namespace, Resource, fields
from api.db import get_connection


ns = Namespace("weather/stats", description="Yearly weather statistics")

weather_stats_model = ns.model(
    "WeatherStats",
    {
        "station_id": fields.String,
        "year": fields.Integer,
        "avg_max_temp": fields.Float,
        "avg_min_temp": fields.Float,
        "total_precipitation": fields.Float,
    },
)

response_model = ns.model(
    "WeatherStatsResponse",
    {
        "data": fields.List(fields.Nested(weather_stats_model)),
        "page": fields.Integer,
        "limit": fields.Integer,
        "total": fields.Integer,
    },
)

def validate_year(year_str: str):
    if not year_str.isdigit() or len(year_str) != 4:
        from flask_restx import abort
        abort(400, "Invalid year format. Expected YYYY.")

@ns.route("")
class WeatherStats(Resource):
    @ns.param('station_id', 'Weather station ID')
    @ns.param('year', 'Year (YYYY)', type=int)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('limit', 'Records per page', type=int, default=20)
    #@ns.marshal_list_with(weather_stats_model)
    def get(self):
        station_id = request.args.get("station_id")
        year = request.args.get("year", type=int)

        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)
        offset = (page - 1) * limit

        where_clauses = []
        params = []

        if station_id:
            where_clauses.append("station_id = %s")
            params.append(station_id)

        if year:
            where_clauses.append("year = %s")
            params.append(year)

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        data_query = f"""
            SELECT
                station_id,
                year,
                avg_max_temp_c AS avg_max_temp,
                avg_min_temp_c AS avg_min_temp,
                total_precip_cm AS total_precipitation
            FROM weather.weather_yearly_stats
            {where_sql}
            ORDER BY year
            LIMIT %s OFFSET %s
        """

        count_query = f"""
            SELECT COUNT(*) AS total
            FROM weather.weather_yearly_stats
            {where_sql}
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(data_query, params + [limit, offset])
        rows = cursor.fetchall()

        cursor.execute(count_query, params)
        total = cursor.fetchone()["total"]

        cursor.close()
        conn.close()

        return {
            "data": rows,
            "page": page,
            "limit": limit,
            "total": total,
        }
