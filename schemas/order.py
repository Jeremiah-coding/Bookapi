from pydantic import BaseModel, ConfigDict, Field

from .book import BookResponse


class OrderCreate(BaseModel):
	customer_name: str = Field(min_length=1, max_length=255)
	book_id: int = Field(gt=0)
	quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	customer_name: str
	book_id: int
	quantity: int
	status: str
	book: BookResponse
