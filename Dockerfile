FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY req.txt /app/req.txt

RUN pip install --no-cache-dir --upgrade -r /app/req.txt

COPY . /app/
