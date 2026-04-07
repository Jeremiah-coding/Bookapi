from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas import OrderCreate, OrderResponse
from services.orders import create_order, list_orders
from tasks.order_tasks import send_order_confirmation

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderResponse])
async def list_orders_route(db: AsyncSession = Depends(get_db)):
    return await list_orders(db)


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order_route(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    new_order = await create_order(db, order)
    background_tasks.add_task(
        send_order_confirmation,
        order_id=new_order.id,
        customer_name=new_order.customer_name,
        book_title=new_order.book.title,
        quantity=new_order.quantity,
    )
    return new_order