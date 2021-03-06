from sqlalchemy import INTEGER, Column, ForeignKey, String, UnicodeText, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(INTEGER(), primary_key=True)


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


class CovidResource(BaseModel):
    __tablename__ = "resources"
    category = Column(String(64))
    city = Column(String(64))
    contact = Column(Text(collation='utf8mb4_unicode_ci'))
    description = Column(Text(collation='utf8mb4_unicode_ci'))
    organisation = Column(Text(collation='utf8mb4_unicode_ci'))
    phone = Column(Text(collation='utf8mb4_unicode_ci'))
    #id = Column(String(16), primary_key=True)
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
