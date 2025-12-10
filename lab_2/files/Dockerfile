#FROM python:3.9-slim

#WORKDIR /app

#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

#COPY /local_model ./local_model
#COPY predict.py .

#RUN groupadd -r appuser && useradd -r -g appuser appuser && \
#    mkdir -p /app /home/appuser/.cache && \
#    chown -R appuser:appuser /app /home/appuser/

#USER appuser

#ENTRYPOINT ["python3", "predict.py"]

FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3.9 python3-pip

WORKDIR /app

COPY predict.py .
COPY /local_model ./local_model
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#подразумевается что predict.py отслеживает stdin
CMD ["python3", "predict.py"]