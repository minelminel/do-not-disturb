FROM alpine:latest

RUN apk update && apk upgrade && \
    apk add python3

COPY requirements.txt .
RUN python3 -m pip install -U pip wheel setuptools && \
    python3 -m pip install -r requirements.txt

WORKDIR /app
COPY . .

CMD ["python3", "-m", "app"]
