from re import M
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CovidResource
import models
import httpx

engine = create_engine(
    "mysql+pymysql://admin:mysqluser@sample-rds.cb1iygfrr3j4.us-east-2.rds.amazonaws.com/covid"
)
models.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
# async with httpx.AsyncClient() as client:
#     res = await client.get('https://api.covid19india.org/resources/resources.json')
resources = []
with httpx.Client() as client:
    res = client.get("https://api.covid19india.org/resources/resources.json").json()
    for entry in res["resources"]:
        resources.append(CovidResource(
            category=entry["category"],
            city=entry["city"],
            contact=entry["contact"],
            description=str(entry["descriptionandorserviceprovided"], 'utf-8'),
            organisation=entry["nameoftheorganisation"],
            phone=entry["phonenumber"],
            state=entry["state"]
        ))
    session.add_all(resources)
    session.commit()