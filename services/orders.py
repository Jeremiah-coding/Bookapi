from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models.book import Book
from models.order import Order
from schemas import OrderCreate


async def list_orders(db: AsyncSession) -> list[Order]:
    result = await db.execute(select(Order).options(selectinload(Order.book)))
    return list(result.scalars().all())


async def create_order(db: AsyncSession, order_data: OrderCreate) -> Order:
    result = await db.execute(select(Book).where(Book.id == order_data.book_id))
    book = result.scalar_one_or_none()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    if book.stock < order_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock",
        )

    book.stock -= order_data.quantity

    new_order = Order(
        customer_name=order_data.customer_name,
        book_id=order_data.book_id,
        quantity=order_data.quantity,
        status="confirmed",
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    await db.refresh(new_order, attribute_names=["book"])

    return new_order
