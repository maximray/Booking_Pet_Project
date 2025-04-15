import pytest
from httpx import AsyncClient

""" Необходимо протестировать CRUD операции с бронированиями:
 Добавление брони (данная операция возвращает id добавленной записи)
 Чтение брони (используя полученный id)
 Удаление брони
 Чтение брони (необходимо убедиться, что бронь удалилась"""

@pytest.mark.parametrize("room_id, date_from, date_to, status_code_a, status_code_r, status_code_d",[ 
    *[(1, "2040-05-15", "2040-05-30", 200, 200, 204)]*20
])
async def test_CRUD(room_id, date_from, date_to, status_code_a, status_code_r, status_code_d, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code_a
    response = response.json()["id"]
    
    response_r = await authenticated_ac.get("/bookings")

    assert response_r.status_code == status_code_r

    response_r = [booking for booking in response_r.json() if booking["id"] == response]

    response_d = await authenticated_ac.delete(f"/bookings/{response_r[0]["id"]}", params={
        "booking_id": response_r[0]["id"]
    })

    assert response_d.status_code == status_code_d

    response_r = await authenticated_ac.get("/bookings")
    response_r = [booking for booking in response_r.json() if booking["id"] == response]
    assert response_r == []
