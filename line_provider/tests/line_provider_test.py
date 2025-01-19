import time

import pytest
from httpx import AsyncClient


@pytest.mark.order(1)
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_simple_workflow(anyio_backend):
    test_id = 'test_id'

    test_event = {
        'id': test_id,
        'coefficient': "1.0",
        'deadline': int(time.time()) + 600,
        'state': 1
    }

    async with AsyncClient(base_url='http://localhost:8000') as ac:
        create_response = await ac.put('/event', json=test_event)

    assert create_response.status_code == 201

    async with AsyncClient(base_url='http://localhost:8000') as ac:
        response = await ac.get(f'/event/{test_id}')

    assert response.status_code == 200
    assert response.json() == test_event

    updated_event = test_event.copy()
    updated_event['state'] = 2

    async with AsyncClient(base_url='http://localhost:8000') as ac:
        update_response = await ac.put('/event', json={'id': test_id, 'state': 2})

    assert update_response.status_code == 201

    async with AsyncClient(base_url='http://localhost:8000') as ac:
        response = await ac.get(f'/event/{test_id}')

    assert response.status_code == 200
    assert response.json() == updated_event
