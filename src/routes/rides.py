from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime

from src.db import get_session
from src.models import Ride, UserRides
from src.schemas import RideCreate, RideUpdate, RideResponse, UserRidesCreate, UserRidesResponse

rides_router = APIRouter(prefix="/rides", tags=["Rides"])


@rides_router.post("/", response_model=RideResponse, status_code=201)
async def create_ride(ride: RideCreate, db: AsyncSession = Depends(get_session)):
    db_ride = Ride(**ride.dict(), dt_created_at=datetime.utcnow())
    db.add(db_ride)
    await db.commit()
    await db.refresh(db_ride)
    return db_ride


@rides_router.get("/", response_model=List[RideResponse])
async def list_rides(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Ride))
    return result.scalars().all()


@rides_router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(ride_id: int, db: AsyncSession = Depends(get_session)):
    ride = await db.get(Ride, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Trajet introuvable.")
    return ride


@rides_router.put("/{ride_id}", response_model=RideResponse)
async def update_ride(ride_id: int, ride_update: RideUpdate, db: AsyncSession = Depends(get_session)):
    ride = await db.get(Ride, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Trajet introuvable.")

    for field, value in ride_update.dict(exclude_unset=True).items():
        setattr(ride, field, value)

    await db.commit()
    await db.refresh(ride)
    return ride


@rides_router.delete("/{ride_id}", status_code=204)
async def delete_ride(ride_id: int, db: AsyncSession = Depends(get_session)):
    ride = await db.get(Ride, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Trajet introuvable.")

    await db.delete(ride)
    await db.commit()
    return None


# --- GESTION DES INSCRIPTIONS À UN TRAJET --- #

@rides_router.post("/{ride_id}/users/", response_model=UserRidesResponse, status_code=201)
async def add_user_to_ride(ride_id: int, user_ride: UserRidesCreate, db: AsyncSession = Depends(get_session)):
    # Optionnel : vérifier existence ride + user ici
    new_link = UserRides(ride_id=ride_id, **user_ride.dict())
    db.add(new_link)
    await db.commit()
    await db.refresh(new_link)
    return new_link


@rides_router.get("/{ride_id}/users/", response_model=List[UserRidesResponse])
async def get_users_from_ride(ride_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(UserRides).where(UserRides.ride_id == ride_id))
    return result.scalars().all()
