from typing import TYPE_CHECKING

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from .order import Order


class Book(Base):
    # Book model; for the database table
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    author: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="book")

