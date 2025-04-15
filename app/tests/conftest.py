import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.bookings.models import Bookings
from app.config import Setting
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert Setting.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)
        
    hotels = open_mock_json("hotels")
    users = open_mock_json("users")
    rooms = open_mock_json("rooms")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_users = insert(Users).values(users)
        add_rooms = insert(Rooms).values(rooms)
        add_bookings = insert(Bookings).values(bookings)
        
        await session.execute(add_hotels)
        await session.execute(add_users)
        await session.execute(add_rooms)
        await session.execute(add_bookings)

        await session.commit()
    




@pytest.fixture(scope="function")
async def ac(): #async client
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(base_url="http://test", transport=transport) as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session 


@pytest.fixture(scope="session")
async def authenticated_ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(base_url="http://test", transport=transport) as ac:
        await ac.post("/auth/login", json={
            "email": "user@example.com",
            "password": "string",
        })

        assert ac.cookies["booking_access_token"]
        yield ac

