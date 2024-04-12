FROM python:3.11.8-slim

WORKDIR /app

# Create a directory for the certificates
RUN mkdir -p /app/certs

COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80 443

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--port", "443", "--cert", "/etc/letsencrypt/live/jpe130.x310.net/fullchain.pem", "--key", "/etc/letsencrypt/live/jpe130.x310.net/privkey.pem"]