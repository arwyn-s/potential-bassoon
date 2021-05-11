from operator import and_
from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine

# import logging

from sqlalchemy.util.compat import local_dataclass_fields

# logger = logging.getLogger(__name__)
app = Sanic("my_app")

bind = create_async_engine(
    "mysql+aiomysql://admin:mysqluser@sample-rds.cb1iygfrr3j4.us-east-2.rds.amazonaws.com/covid",
    echo=True,
)

# ./server.py
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

_base_model_session_ctx = ContextVar("session")


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = sessionmaker(bind, AsyncSession, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


# ./server.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sanic.response import json

from models import CovidResource


# @app.post("/user")
# async def create_user(request):
#     session = request.ctx.session
#     async with session.begin():
#         car = Car(brand="Tesla")
#         person = Person(name="foo", cars=[car])
#         session.add_all([person])
#     return json(person.to_dict())

# @app.get("/update")
# async def create_user(request):
#     session = request.ctx.session
#     resources.
#     async with httpx.AsyncClient() as client:
#         res = await client.get('https://api.covid19india.org/resources/resources.json')
#     async with session.begin():


@app.get("/cities")
async def get_all_cities(request):
    session = request.ctx.session
    async with session.begin():
        stmt = select(CovidResource.city).distinct()
        result = await session.execute(stmt)
        cities = result.all()
        # print(cities)
        # session.add_all([person])
    return json({"data": [city[0] for city in cities]})


@app.get("/categories")
async def get_all_categories(request):
    session = request.ctx.session
    async with session.begin():
        stmt = select(CovidResource.category).distinct()
        result = await session.execute(stmt)
        categories = result.all()
        # session.add_all([person])
    return json({"data": [cat[0] for cat in categories]})


@app.get("/resource")
async def guery_resource(request):
    session = request.ctx.session
    city = request.args.get("city", None)
    category = request.args.get("category", None)
    async with session.begin():
        if city and category:
            stmt = select(CovidResource).where(
                and_(CovidResource.city == city, CovidResource.category == category)
            )
        elif city:
            stmt = select(CovidResource).where(CovidResource.city == city)
        elif category:
            stmt = select(CovidResource).where(CovidResource.category == category)
        else:
            stmt = select(CovidResource)

        result = await session.execute(stmt)
        # print(result)
        data = result.all()
        # print(data)
        # session.add_all([person])
    return json({"data": [resource[0].to_dict() for resource in data]})


# @app.get("/user/<pk:int>")
# async def get_user(request, pk):
#     session = request.ctx.session
#     async with session.begin():
#         stmt = select(Person).where(Person.id == pk).options(selectinload(Person.cars))
#         result = await session.execute(stmt)
#         person = result.scalar()

#     if not person:
#         return json({})

#     return json(person.to_dict())


app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
