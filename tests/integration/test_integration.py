import asyncpg
import requests
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'taskmanager_service/app'))
sys.path.append(str(BASE_DIR / 'randomquote_service/app'))

from taskmanager_service.app.main import service_alive as taskmanager_status
from randomquote_service.app.main import service_alive as randomquote_status

@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect("postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query")
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"

@pytest.mark.asyncio
async def test_quotes_api():
    r = requests.get("https://api.quotable.io/random")
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_taskmanager_service_connection():
    r = await taskmanager_status()
    assert r == {'message': 'service alive'}

@pytest.mark.asyncio
async def test_randomquote_service_connection():
    r = await randomquote_status()
    assert r == {'message': 'service alive'}