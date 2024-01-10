FROM python:latest
WORKDIR /app

COPY DNSUpdater.py /app/DNSUpdater.py
COPY config.json /app/config.json
COPY requirements.txt /app/requirements.txt
COPY crontab /etc/cron.d/crontab

RUN apt-get update && apt-get -y install cron && \
    pip3 install -r /app/requirements.txt && \
    chmod 0644 /etc/cron.d/crontab && \
    /usr/bin/crontab /etc/cron.d/crontab

RUN /usr/local/bin/python3 /app/DNSUpdater.py

CMD ["cron", "-f"]
