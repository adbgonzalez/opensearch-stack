FROM python:3.11-slim
WORKDIR /app

# dependencias do producer
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# código do producer
COPY . /app

CMD ["sleep","infinity"]