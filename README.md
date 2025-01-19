### BWS

Система, принимающая ставки на какие-либо события, состоящая из двух микросервисов (**line_provider** и  **bet_maker** )
```
docker-compose up -d
```

* line_provider будет доступен на порту **8000**.
* bet_maker будет доступен на порту **8001**.

Документация к микросервисам:

* line_provider: http://localhost/8000/docs
* bet_maker: http://localhost/8001/docs

Для запуска интеграционных тестов: 

* Установить pytest, pytest-order, pytest-asyncio, anyio, httpx:
```
pip install pytest pytest-order pytest-asyncio anyio httpx
```
При работаюших сервисах запустить pytest из корня проекта:

```
pytest
```