FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY abuseipdb/ abuseipdb/
COPY check_ip/ check_ip/

CMD ["python","-m", "check_ip.main"]