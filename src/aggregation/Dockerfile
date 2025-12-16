FROM python:3.11-slim

WORKDIR /app

COPY aggregation/ aggregation/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "aggregation/populate_weather_yearly_stats.py"]
