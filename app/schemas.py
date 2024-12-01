from typing import Any
from pydantic import BaseModel, field_validator


class CreateProductIn(BaseModel):
    quantity: int
    price: int
    name: str

    @field_validator('quantity', 'price', mode="before")
    def validate_nums(cls, v):
        try:
            return int(v)
        except:
            raise ValueError("Quantity and price must be numbers")