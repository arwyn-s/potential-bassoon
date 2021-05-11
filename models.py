from sqlalchemy import INTEGER, Column, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# class BaseModel(Base):
#     __abstract__ = True
#     id = Column(INTEGER(), primary_key=True)


# class Person(BaseModel):
#     __tablename__ = "person"
#     name = Column(String(16))
#     cars = relationship("Car")

#     def to_dict(self):
#         return {"name": self.name, "cars": [{"brand": car.brand} for car in self.cars]}


# class Car(BaseModel):
#     __tablename__ = "car"

#     brand = Column(String(16))
#     user_id = Column(ForeignKey("person.id"))
#     user = relationship("Person", back_populates="cars")


class CovidResource(Base):
    __tablename__ = "resources"
    category = Column(String(64))
    city = Column(String(64))
    contact = Column(String(64))
    description = Column(String(256))
    organisation = Column(String(128))
    phone = Column(String(64))
    state = Column(String(64))

    def to_dict(self):
        return {
            "category": self.category,
            "city": self.city,
            "contact": self.contact,
            "description": self.description,
            "organisation": self.organisation,
            "phone": self.phone,
            "state": self.state,
        }
