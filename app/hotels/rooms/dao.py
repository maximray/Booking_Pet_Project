from datetime import date

from sqlalchemy import select

from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import NoHotelByID
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.utils.room_utils import calculate_rooms_pre_left


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_by_hotels(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            hotels_query = select(Hotels).filter_by(id=hotel_id)
            hotels = await session.execute(hotels_query)
            hotels = hotels.scalars()

            result = []
            for hotel in hotels:
                rooms_query = select(cls.model).filter_by(hotel_id=hotel.id)
                rooms = await session.execute(rooms_query)
                rooms = rooms.scalars()

                for room in rooms:
                    rooms_pre_left = await calculate_rooms_pre_left(
                        session, room.id, date_from, date_to
                    )

                    result.append({
                        
                            "id": room.id,
                            "hotel_id": room.hotel_id,
                            "name": room.name,
                            "description": room.description,
                            "services": room.services,
                            "price": room.price,
                            "quantity": room.quantity,
                            "image_id": room.image_id,
                            "total_cost": (date_to - date_from).days * room.price,
                            "rooms_left": rooms_pre_left,
                        
                    })

            if not result:
                raise NoHotelByID
            return result
