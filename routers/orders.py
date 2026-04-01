from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from models.book import Order
from schemas import OrderCreate, OrderResponse
from services.orders import create_order

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderResponse])
async def list_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    return result.scalars().all()


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order_route(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_order(db, order)