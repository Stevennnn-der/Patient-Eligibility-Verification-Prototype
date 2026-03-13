from pydantic import BaseModel, Field
from typing import Optional


class Patient(BaseModel):
    first_name: str = Field(..., example="Michael")
    last_name: str = Field(..., example="Motorist")
    dob: str = Field(..., example="1978-03-08")
    gender: Optional[str] = Field(None, example="M")
    address: Optional[str] = Field(None, example="345 Anywhere Street, Your City, NY 12345")