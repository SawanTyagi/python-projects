from fastapi import APIRouter, Query, Path, Body

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from ..model_classes.user import User
from ..model_classes.item import Item

router = APIRouter()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@router.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]


@router.post('/items/')
async def create_item(item: Item):
    return item


@router.put('/items/{item_id}')
async def update_item(item_id: Annotated[int, Path(title="The ID of item to get")],
                      item: Annotated[Item, Body(examples=[
                          {
                              "name": "Foo",
                              "description": "A very nice Item",
                              "price": 35.4,
                              "tax": 3.2,
                          },
                          {
                              "name": "Bar",
                              "price": "35.4",
                          },
                          {
                              "name": "Baz",
                              "price": "thirty five point four",
                          },
                      ], )],
                      q: Annotated[str | None, Query(max_length=50, min_length=3)] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@router.get('/items_with_query_parameter_multiple_values/')
async def items_with_query_parameter_multiple_values(
        q: Annotated[list[str] | None, Query(max_length=50, min_length=3)] = None):
    return {"q": q}


class FilterModel(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@router.get("/getQueryModelParams")
async def get_query_model_param(query_filter: Annotated[FilterModel, Query()]):
    return query_filter


@router.post('/mix-query-path-body-parameter/{item_id}')
async def mix_query_path_body_parameter(
        item_id: int,
        item: Item,
        user: User,
        importance: Annotated[int, Body(gt=0)],
        q: str | None = None):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
