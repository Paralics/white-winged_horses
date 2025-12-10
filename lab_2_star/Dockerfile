FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /local_model ./local_model

COPY app_requirements.txt .
RUN pip install --no-cache-dir -r app_requirements.txt

COPY predict_app.py .

RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p /app /home/appuser/.cache && \
    chown -R appuser:appuser /app /home/appuser/

USER appuser

ENTRYPOINT ["python3", "predict_app.py"]