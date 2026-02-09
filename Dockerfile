FROM python:3.14-alpine

RUN apk update && apk add --no-cache uv

WORKDIR /app

COPY pip/requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY src ./src

CMD ["python", "src/main.py"]
