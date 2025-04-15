from datetime import date


from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms as (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2033-05-15' AND date_from <= '2033-06-20') OR
            (date_from <= '2033-05-15' AND date_to > '2033-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left = await session.execute(rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()

                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"

            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to
                }
            logger.error(
                msg, extra=extra, exc_info=True
            )

    @classmethod
    async def get_all_bookings(cls, user_id):
        async with async_session_maker() as session:
            # Создаем запрос с JOIN для объединения Bookings и Rooms
            query = (
                select(
                    cls.model.id.label("booking_id"),
                    cls.model.room_id,
                    cls.model.user_id,
                    cls.model.date_from,
                    cls.model.date_to,
                    cls.model.price,
                    cls.model.total_cost,
                    cls.model.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .join(
                    Rooms, Rooms.id == cls.model.room_id
                )  # JOIN по связи room_id -> id
                .filter(cls.model.user_id == user_id)  # Фильтруем по user_id
            )

            bookings = await session.execute(query)
            results = bookings.mappings().all()  # Получаем данные в виде маппинга

            # Форматируем результат
            formatted_results = [
                {
                    "id": mapping["booking_id"],
                    "room_id": mapping["room_id"],
                    "user_id": mapping["user_id"],
                    "date_from": mapping["date_from"].isoformat(),
                    "date_to": mapping["date_to"].isoformat(),
                    "price": mapping["price"],
                    "total_cost": mapping["total_cost"],
                    "total_days": mapping["total_days"],
                    "image_id": mapping["image_id"],
                    "name": mapping["name"],
                    "description": mapping["description"],
                    "services": mapping["services"],
                }
                for mapping in results
            ]

            return formatted_results

    @classmethod
    async def delete_booking(cls, booking_id, user_id):
        async with async_session_maker() as session:
            # Создаем запрос для удаления бронирования
            query = (
                delete(cls.model)
                .where(cls.model.id == booking_id)
                .where(
                    cls.model.user_id == user_id
                )  # Убедимся, что бронирование принадлежит пользователю
            )

            result = await session.execute(query)  # Выполняем запрос
            await session.commit()  # Фиксируем изменения
