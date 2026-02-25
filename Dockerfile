FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask requests gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
