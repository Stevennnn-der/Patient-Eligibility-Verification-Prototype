from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.patient import Patient
from app.models.insurance import Insurance


class Provider(BaseModel):
    npi: str = Field(..., example="1234567893")
    organization: Optional[str] = Field(None, example="iClinic")


class WarningMessage(BaseModel):
    field: Optional[str] = Field(None, example="insurance.group_number")
    message: str = Field(..., example="Extracted with low confidence")


class ExtractionResponse(BaseModel):
    patient: Optional[Patient] = None
    insurance: Optional[Insurance] = None
    provider: Optional[Provider] = None
    service_date: Optional[str] = Field(None, example="2024-01-01")
    warnings: List[WarningMessage] = []


class EligibilityRequest(BaseModel):
    patient: Patient
    insurance: Insurance
    provider: Provider
    service_date: str = Field(..., example="2024-01-01")


class CopaySummary(BaseModel):
    general_visit: Optional[float] = Field(None, example=23)
    specialist_visit: Optional[float] = Field(None, example=25)
    emergency_visit: Optional[float] = Field(None, example=150)
    deductible: Optional[float] = Field(None, example=300)


class PharmacySummary(BaseModel):
    enabled: bool = Field(..., example=True)
    rx_bin: Optional[str] = Field(None, example="610279")
    rx_pcn: Optional[str] = Field(None, example="9999")


class EligibilitySummary(BaseModel):
    coverage_active: bool = Field(..., example=True)
    payer: Optional[str] = Field(None, example="UnitedHealthcare")
    member_id: Optional[str] = Field(None, example="123456789")
    service_date: Optional[str] = Field(None, example="2024-01-01")
    copay: Optional[CopaySummary] = None
    pharmacy: Optional[PharmacySummary] = None
    raw_271_reference: Optional[str] = Field(None, example="mock-response-001")


class EligibilityResponse(BaseModel):
    raw_271: str
    summary: EligibilitySummary


class Parse271Request(BaseModel):
    raw_271: str


class ErrorResponse(BaseModel):
    error: str = Field(..., example="validation_failed")
    details: List[str] = Field(default_factory=list, example=["insurance.member_id is required"])
    
class WorkflowEligibilityResponse(BaseModel):
    extracted_data: ExtractionResponse
    eligibility_result: EligibilityResponse