from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.db import get_session
from src.models import Bike
from src.schemas import BikeCreate, BikeUpdate, BikeResponse

bikes_router = APIRouter(prefix="/bikes", tags=["Bikes"])

@bikes_router.post("/", response_model=BikeResponse, status_code=201)
async def create_bike(bike: BikeCreate, db: AsyncSession = Depends(get_session)):
    db_bike = Bike(**bike.dict())
    db.add(db_bike)
    await db.commit()
    await db.refresh(db_bike)
    return db_bike


@bikes_router.get("/", response_model=List[BikeResponse])
async def list_bikes(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Bike))
    return result.scalars().all()


@bikes_router.get("/{bike_id}", response_model=BikeResponse)
async def get_bike(bike_id: int, db: AsyncSession = Depends(get_session)):
    bike = await db.get(Bike, bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Moto introuvable.")
    return bike


@bikes_router.put("/{bike_id}", response_model=BikeResponse)
async def update_bike(bike_id: int, bike_update: BikeUpdate, db: AsyncSession = Depends(get_session)):
    bike = await db.get(Bike, bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Moto introuvable.")

    for field, value in bike_update.dict(exclude_unset=True).items():
        setattr(bike, field, value)

    await db.commit()
    await db.refresh(bike)
    return bike


@bikes_router.delete("/{bike_id}", status_code=204)
async def delete_bike(bike_id: int, db: AsyncSession = Depends(get_session)):
    bike = await db.get(Bike, bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Moto introuvable.")

    await db.delete(bike)
    await db.commit()
    return None
