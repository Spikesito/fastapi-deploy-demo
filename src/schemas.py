from pydantic import BaseModel, validator
from typing import Optional
from datetime import date


# Schémas pour User
class UserBase(BaseModel):
    username: str
    email: str
    date_of_birth: Optional[str] = None  # Stocke la date sous forme de chaîne

    @validator("date_of_birth", pre=True, always=True)
    def format_date_of_birth(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[str] = None

    @validator("date_of_birth", pre=True, always=True)
    def format_date_of_birth(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v

class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True


# Schémas pour Bike
class BikeBase(BaseModel):
    lb_brand: str
    lb_model: str
    dt_immatriculation: Optional[str] = None  # Stocke la date sous forme de chaîne

    @validator("dt_immatriculation", pre=True, always=True)
    def format_dt_immatriculation(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v


class BikeCreate(BikeBase):
    owner_id: int


class BikeUpdate(BaseModel):
    lb_brand: Optional[str] = None
    lb_model: Optional[str] = None
    dt_immatriculation: Optional[str] = None

    @validator("dt_immatriculation", pre=True, always=True)
    def format_dt_immatriculation(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v

class BikeResponse(BikeBase):
    bike_id: int
    owner_id: int

    class Config:
        orm_mode = True



# Schémas pour Ride et UserRides

class RideBase(BaseModel):
    lb_title: str
    lb_description: Optional[str]
    nb_max_members: int
    lb_location: str
    dt_start: str
    
    @validator("dt_start", pre=True, always=True)
    def format_dt_immatriculation(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v

class RideCreate(RideBase):
    pass

class RideUpdate(BaseModel):
    lb_title: Optional[str]
    lb_description: Optional[str]
    nb_max_members: Optional[int]
    lb_location: Optional[str]
    dt_start: Optional[str]
    
    @validator("dt_start", pre=True, always=True)
    def format_dt_immatriculation(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v

class RideResponse(RideBase):
    ride_id: int
    dt_created_at: str

    @validator("dt_created_at", pre=True, always=True)
    def format_dt_created_at(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v

    class Config:
        orm_mode = True


class UserRidesBase(BaseModel):
    creator_id: int
    role: Optional[str]

class UserRidesCreate(UserRidesBase):
    pass

class UserRidesResponse(UserRidesBase):
    ride_id: int

    class Config:
        orm_mode = True



# Schémas pour messages

class MessageBase(BaseModel):
    lb_content: str
    author_id: int
    ride_id: int

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    lb_content: Optional[str]

class MessageResponse(MessageBase):
    message_id: int

    class Config:
        orm_mode = True