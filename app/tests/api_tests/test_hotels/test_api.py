import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location, date_from, date_to, status_code",[
    ("Алтай", "2030-05-15", "2030-05-30", 200),
    ("Алтай", "2030-05-15", "2030-06-30", 400),
    ("Алтай", "2030-06-15", "2030-05-30", 400),

])
async def test_get_all_hotels(location, date_from, date_to, status_code, ac: AsyncClient):
    response = await ac.get(f"/hotels/{location}", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code