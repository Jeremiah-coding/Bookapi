from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from models.book import Book
from schemas import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookResponse])
async def list_books_route(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    return list(result.scalars().all())


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book_route(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(
        title=book.title,
        author=book.author,
        price=book.price,
        stock=book.stock,
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book
