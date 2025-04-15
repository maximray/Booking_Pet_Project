from datetime import date

from fastapi import APIRouter, Query, status

from app.exceptions import IncorrectDate
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SGetHotels, SGetSpecificHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)



@router.get("/{location}", status_code=status.HTTP_200_OK, description="Возвращает список отелей по заданным параметрам, причем в отеле должен быть минимум 1 свободный номер")
#@cache(expire=20) #из за него не показывает пример вывода, показывает string
async def get_all_hotels(
    location: str,
    date_from: date = Query(description="Например, 2023-03-18"),
    date_to: date = Query(description="Например, 2023-03-18"),
    ) -> list[SGetHotels]:
    diff_date = (date_to - date_from).days
    if date_from >= date_to or diff_date > 30:
        raise IncorrectDate
    
    return await HotelDAO.find_all(location=location,date_from=date_from,date_to=date_to)


@router.get("/id/{hotel_id}", status_code=status.HTTP_200_OK, description="Возвращает все данные по одному отелю")
async def get_specific_hotel(
    hotel_id: int,
) -> list[SGetSpecificHotel]: 
    return await HotelDAO.get_specific_hotel(hotel_id=hotel_id)

