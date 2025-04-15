import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code",[
    *[(1, "2030-05-01","2030-05-15", i, 200) for i in range(3, 8)],
    (1, "2030-05-01","2030-05-15", 7, 409),
    (1, "2030-05-01","2030-05-15", 7, 409)
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code, booked_rooms, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms


