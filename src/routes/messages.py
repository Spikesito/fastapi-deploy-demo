from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.db import get_session
from src.models import Message
from src.schemas import MessageCreate, MessageUpdate, MessageResponse

messages_router = APIRouter(prefix="/messages", tags=["Messages"])


@messages_router.post("/", response_model=MessageResponse, status_code=201)
async def create_message(message: MessageCreate, db: AsyncSession = Depends(get_session)):
    db_message = Message(**message.dict())
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message


@messages_router.get("/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: AsyncSession = Depends(get_session)):
    message = await db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message introuvable.")
    return message


@messages_router.put("/{message_id}", response_model=MessageResponse)
async def update_message(message_id: int, message_update: MessageUpdate, db: AsyncSession = Depends(get_session)):
    message = await db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message introuvable.")

    for field, value in message_update.dict(exclude_unset=True).items():
        setattr(message, field, value)

    await db.commit()
    await db.refresh(message)
    return message


@messages_router.delete("/{message_id}", status_code=204)
async def delete_message(message_id: int, db: AsyncSession = Depends(get_session)):
    message = await db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message introuvable.")

    await db.delete(message)
    await db.commit()
    return None


@messages_router.get("/ride/{ride_id}", response_model=List[MessageResponse])
async def get_messages_for_ride(ride_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Message).where(Message.ride_id == ride_id))
    return result.scalars().all()
