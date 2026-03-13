from pydantic import BaseModel, Field
from typing import Optional


class Insurance(BaseModel):
    payer: str = Field(..., example="UnitedHealthcare")
    member_id: str = Field(..., example="123456789")
    group_number: Optional[str] = Field(None, example="9999")
    plan_code: Optional[str] = Field(None, example="UHEALTH")
    rx_bin: Optional[str] = Field(None, example="610279")
    rx_pcn: Optional[str] = Field(None, example="9999")