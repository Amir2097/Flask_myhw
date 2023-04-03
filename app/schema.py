from typing import Any, Dict, Optional, Type
from errors import HttpError
from pydantic import BaseModel, EmailStr, ValidationError


class CreateItem(BaseModel):
    title: str
    description: str
    owner_id: int


class CreateUser(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]


SCHEMA_TYPE = Type[CreateItem] | Type[CreateUser]


def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
    try:
        validated = schema(**data).dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated
