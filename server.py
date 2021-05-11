from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine

app = Sanic("my_app")

bind = create_async_engine(
    "mysql+aiomysql://admin:mysqluser@sample-rds.cb1iygfrr3j4.us-east-2.rds.amazonaws.com/test",
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

from models import Car, Person


@app.post("/user")
async def create_user(request):
    session = request.ctx.session
    async with session.begin():
        car = Car(brand="Tesla")
        person = Person(name="foo", cars=[car])
        session.add_all([person])
    return json(person.to_dict())


@app.get("/user/<pk:int>")
async def get_user(request, pk):
    session = request.ctx.session
    async with session.begin():
        stmt = select(Person).where(Person.id == pk).options(selectinload(Person.cars))
        result = await session.execute(stmt)
        person = result.scalar()

    if not person:
        return json({})

    return json(person.to_dict())


if __name__ == "main":
    app.run(host="0.0.0.0", port=8005, debug=True, auto_reload=True)
