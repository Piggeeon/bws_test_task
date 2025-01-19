FROM python:3.10

WORKDIR /app

RUN pip install fastapi uvicorn aiohttp

COPY src src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
