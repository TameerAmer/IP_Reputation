FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY abuseipdb/ abuseipdb/
COPY check_ip_batch/ check_ip_batch/

CMD ["python","-m", "check_ip_batch.main"]