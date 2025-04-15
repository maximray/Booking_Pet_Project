
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import Setting
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.users.router_get_user import router as router_users_get
from app.logger import logger
from fastapi_versioning import VersionedFastAPI
from app.prometheus.router import router as router_prometheus
import sentry_sdk


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

sentry_sdk.init(
    dsn="https://75c5861cc335caa49087ed136bb691b6@o4509128290336768.ingest.us.sentry.io/4509128294203392",
    send_default_pii=True,
)


app = FastAPI(lifespan=lifespan)




app.include_router(router_users)
app.include_router(router_users_get)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings) 
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_prometheus)





'''
FOR FRONTEND
'''


# origins = [
#     "http://localhost:8000", #allow address of frontend
# ]


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True, #cookie
#     allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
#     allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
#                    "Access-Control-Allow-Origins", "Authorization"]
# )

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{Setting.REDIS_HOST}:{Setting.REDIS_PORT}", encoding="urf-8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Requests execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

app.mount("/static", StaticFiles(directory="app/static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*","/metrics"]
)
instrumentator.instrument(app).expose(app)