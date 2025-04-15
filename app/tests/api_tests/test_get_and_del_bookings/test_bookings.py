import pytest
from httpx import AsyncClient


async def test_get_and_del_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")
    assert response.status_code == 200
    

    for booked in response.json():
        booking_id = booked["id"]
        response_two = await authenticated_ac.delete(f"/bookings/{booking_id}", params={
            "booking_id": booking_id
        })
        assert response_two.status_code == 204
        
        
    response = await authenticated_ac.get("/bookings")
    assert response.json() == "No rooms booked"
    
    