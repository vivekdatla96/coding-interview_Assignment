from flask import Flask
from flask_restx import Api
from api.routes.weather import ns as weather_ns
from api.routes.weather_stats import ns as weather_stats_ns

def create_app(testing: bool = False):
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True

    api = Api(
        app,
        title="Weather API",
        version="1.0",
        description="Weather and Weather Statistics API",
        doc="/swagger"
    )

    api.add_namespace(weather_ns, path="/api/weather")
    api.add_namespace(weather_stats_ns, path="/api/weather/stats")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
