from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Order(Base):
    """Order model; for the database table, id, customer name, book id, status, primary key is id. all values are required."""
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    book: Mapped["Book"] = relationship("Book", back_populates="orders")
