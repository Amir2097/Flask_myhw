from typing import Any, Dict, Optional, Type
from errors import HttpError
from pydantic import BaseModel, EmailStr, ValidationError, validator
import re

password_regex = re.compile("^(?=.*[a-z_])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,50}$")


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class RegisterUser(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValidationError('password is to easy')
        return value


class CreateItem(BaseModel):
    title: str
    description: str
    owner_id: int


class CreateUser(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]


class AdsData(BaseModel):

    ad_header: Optional[str]
    description: Optional[str]


SCHEMA_TYPE = Type[CreateItem] | Type[CreateUser] | Type[AdsData] | Type[LoginUser] | Type[RegisterUser]


def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
    try:
        validated = schema(**data).dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated
