from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    phone_number: Optional[str]


class Authorization(BaseModel):
    email: str
    password: str
