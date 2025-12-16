# Code Challenge Template
This project implements an end-to-end weather data pipeline that ingests historical weather observations, aggregates yearly statistics, and exposes the data through a RESTful API.

The solution is designed with scalability, testability, and cloud deployment in mind and follows industry best practices for data engineering and API development.

Raw Weather Files
        │
        ▼
Ingestion (Python)
        │
        ▼
MySQL (weather table)
        │
        ▼
Aggregation (Yearly Stats)
        │
        ▼
MySQL (weather_yearly_stats)
        │
        ▼
REST API (Flask + Swagger)

Local Setup Guide
1. Prerequisites
Before starting, ensure the following are installed on your system:
    Python 3.10+
    MySQL 8.x
    Git
    (Optional but recommended) Docker

2. Clone the Repository
    git clone https://github.com/vivekdatla96/coding-interview_Assignment
    cd code-challenge-template

3. Create and Activate Python Virtual Environment
    python -m venv venv
    venv\Scripts\activate

4. Install Python Dependencies
    pip install --upgrade pip
    pip install -r src/requirements.txt

5. Set Up MySQL Database
 Run the each scripts mentioned in db/init folder in numberical order

6. Run Data Ingestion
    Place raw weather files into the input directory (as specified in ingestion code).
    Bash Script:
    cd src
    python ingestion/load_weather.py

7. Run Aggregation (Yearly Statistics)
    python src\aggregation\populate_weather_yearly_stats.py

8. Start the REST API
    python api/app.py
    API will be available at: http://localhost:5000

9. Test Using Swagger UI
    http://localhost:5000/swagger
    
10. Run Unit Tests
    pytest -v


Data Pipeline
Ingestion
    Parses raw weather files
    Validates records
    Loads data into MySQL
    Handles missing or invalid values gracefully
    Idempotent (safe to re-run)
Aggregation
 Computes yearly averages and totals
    Upserts into weather_yearly_stats
    

REST API
1. GET /api/weather
2. GET /api/weather/stats

Author
Vivek Datla
