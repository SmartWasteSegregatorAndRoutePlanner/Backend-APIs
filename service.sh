#!/bin/bash
cd /home/ubuntu/Backend-APIs
source ./venv/bin/activate
gunicorn -b 0.0.0.0:80 backend_api.wsgi --access-logfile logs/access-logs.txt --error-logfile logs/error-log.txt
