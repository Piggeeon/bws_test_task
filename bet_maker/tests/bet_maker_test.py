import pytest
from httpx import AsyncClient


@pytest.mark.order(2)
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_simple_workflow(anyio_backend):
    test_event_id = 'test_id'

    test_bet = {
        "event_id": test_event_id,
        "amount": 500,
    }

    async with AsyncClient(base_url='http://localhost:8001') as ac:
        create_response = await ac.post('/bet', params=test_bet)

    assert create_response.status_code == 201

    async with AsyncClient(base_url='http://localhost:8001') as ac:
        response = await ac.get('/bets')

    assert response.status_code == 200

    new_test_event_state = 2
    async with AsyncClient(base_url='http://localhost:8001') as ac:
        update_response = await ac.patch('/bet', params={'event_id': test_event_id, 'new_state': new_test_event_state})

    assert update_response.status_code == 200

    async with AsyncClient(base_url='http://localhost:8001') as ac:
        updated_response = await ac.get('/bets')

    assert updated_response.status_code == 200

    for bet in updated_response.json():
        if bet["event_id"] == test_event_id:
            print(bet)
            assert bet["status"] == new_test_event_state
