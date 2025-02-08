
FROM python:3.13.0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

CMD ["fastapi", "run", "app/run.py", "--port", "8008"]