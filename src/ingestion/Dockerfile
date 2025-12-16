FROM python:3.11-slim

WORKDIR /app

COPY ingestion/ ingestion/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ingestion/load_weather.py"]