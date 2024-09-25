from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item", max_length=200)
    price: float = Field(ge=0, description="The price must be greater than zero", )
    tax: float | None = None
