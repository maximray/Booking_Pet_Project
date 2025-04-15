from datetime import date

from fastapi import APIRouter, status

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SGetRooms

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"]
)


@router.get("/{hotel_id}/rooms",status_code=status.HTTP_200_OK,description="возвращает список всех номеров определенного отеля")
async def get_rooms_by_hotels(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[SGetRooms]:
    return await RoomDAO.get_rooms_by_hotels(hotel_id=hotel_id, date_from=date_from, date_to=date_to)