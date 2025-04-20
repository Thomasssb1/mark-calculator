FROM python:3.13-slim

WORKDIR /app

COPY . ./

VOLUME ["/app/data"]

ENTRYPOINT [ "python3", "main.py" ]

CMD ["help"]