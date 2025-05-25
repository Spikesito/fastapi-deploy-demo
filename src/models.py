from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON, Table
from sqlalchemy.orm import relationship
from src.db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)

    bikes = relationship("Bike", back_populates="owner")
    rides = relationship("UserRides", back_populates="creator")
    messages = relationship("Message", back_populates="author")
    

class Bike(Base):
    __tablename__ = "bikes"

    bike_id = Column(Integer, primary_key=True, index=True)
    lb_brand = Column(String, nullable=False)
    lb_model = Column(String, nullable=False)
    dt_immatriculation = Column(Date, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.user_id"))
    owner = relationship("User", back_populates="bikes")

#     photos = relationship("Photo", back_populates="bike")

class Ride(Base):
    __tablename__ = "rides"

    ride_id = Column(Integer, primary_key=True, index=True)
    lb_title = Column(String, nullable=False)
    lb_description = Column(String, nullable=True)
    nb_max_members = Column(Integer, nullable=False)
    lb_location = Column(String, nullable=False)
    dt_start = Column(Date, nullable=False)
    dt_created_at = Column(Date, nullable=False)
    
    user_rides = relationship("UserRides", back_populates="ride")
    messages = relationship("Message", back_populates="ride")

class UserRides(Base):
    __tablename__ = "user_rides"

    creator_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    ride_id = Column(Integer, ForeignKey("rides.ride_id"), primary_key=True)
    role = Column(String, nullable=True)

    creator = relationship("User", back_populates="rides")
    ride = relationship("Ride", back_populates="user_rides")

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    lb_content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.user_id"))
    ride_id = Column(Integer, ForeignKey("rides.ride_id"))

    ride = relationship("Ride", back_populates="messages")
    author = relationship("User", back_populates="messages")

# class Photo(Base):
#     __tablename__ = "photos"

#     id = Column(Integer, primary_key=True, index=True)
#     content_file = Column(String, nullable=False)
#     metadata = Column(JSON, nullable=True)

#     bike_id = Column(Integer, ForeignKey("bikes.id"))
#     bike = relationship("Bike", back_populates="photos")

#     conversation_id = Column(Integer, ForeignKey("conversations.id"))
#     conversation = relationship("Conversation", back_populates="photos")