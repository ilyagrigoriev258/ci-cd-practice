FROM python:3.12.7-slim
WORKDIR /app
COPY . /app
CMD ["python", "task_app.py", "--help"]