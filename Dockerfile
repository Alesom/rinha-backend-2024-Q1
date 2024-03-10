FROM python:3.12-alpine

COPY ./ /app/
WORKDIR /app/

RUN pip install -r /app/requirements.txt

CMD exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 1 --log-level error

# CMD exec gunicorn backend.main:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --timeout 3000
