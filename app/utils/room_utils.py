from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms


async def calculate_rooms_pre_left(session, room_id: int, date_from, date_to):
    booked_rooms = select(Bookings).where(
        and_(
            Bookings.room_id == room_id,
            or_(
                and_(
                    Bookings.date_from >= date_from,
                    Bookings.date_from <= date_to
                ),
                and_(
                    Bookings.date_from <= date_from,
                    Bookings.date_to > date_from
                ),
            )
        )
    ).cte("booked_rooms")

    rooms_pre_left_query = select(
        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_pre_left")
    ).select_from(Rooms).join(
        booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
    ).where(Rooms.id == room_id).group_by(
        Rooms.quantity, booked_rooms.c.room_id
    )
    
    rooms_pre_left = await session.execute(rooms_pre_left_query)
    return rooms_pre_left.scalar()
