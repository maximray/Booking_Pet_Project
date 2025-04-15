from datetime import date

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder

from app.bookings.dao import BookingDAO
from app.exceptions import RoomCannotBeBooked, UserIsNotPresentException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi_versioning import version

router = APIRouter(
    prefix='/bookings',
    tags=["Бронирования"]
)


@router.get("", status_code=status.HTTP_200_OK, description='Возвращает список всех бронирований пользователя')
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)):# -> list[SBookings]:
    if not user:
        raise UserIsNotPresentException
    
    booked = await BookingDAO.get_all_bookings(user_id=user.id)
    if not booked:
        return "No rooms booked"
    return booked
    

@router.post("")
@version(2)
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
    ):
    booking = await BookingDAO.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
    if not booking:
        raise RoomCannotBeBooked
    
    send_booking_confirmation_email.delay(jsonable_encoder(booking), user.email)
    return booking

    
@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT, description="Удаляет бронь пользователя")
@version(1)
async def del_booking(
    booking_id : int,
    user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIsNotPresentException

    return await BookingDAO.delete_booking(booking_id=booking_id, user_id=user.id)
    
    