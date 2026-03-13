from fastapi import APIRouter, HTTPException
from app.models.eligibility import (
    EligibilityRequest,
    EligibilityResponse,
    Parse271Request,
)
from app.services.eligibility_service import verify_patient_eligibility
from app.services.edi271_parser import parse_271_message
from app.utils.validators import is_valid_npi, is_valid_date

router = APIRouter()


@router.post("/verify", response_model=EligibilityResponse)
def verify_eligibility(payload: EligibilityRequest):
    if not payload.insurance.member_id:
        raise HTTPException(status_code=422, detail="insurance.member_id is required")

    if not is_valid_npi(payload.provider.npi):
        raise HTTPException(status_code=422, detail="provider.npi must be 10 digits")

    if not is_valid_date(payload.service_date):
        raise HTTPException(status_code=422, detail="service_date must be YYYY-MM-DD")

    raw_271 = verify_patient_eligibility(payload.model_dump())
    summary = parse_271_message(raw_271)

    return EligibilityResponse(
        raw_271=raw_271,
        summary=summary
    )


@router.post("/parse", response_model=EligibilityResponse)
def parse_271(payload: Parse271Request):
    try:
        summary = parse_271_message(payload.raw_271)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return EligibilityResponse(
        raw_271=payload.raw_271,
        summary=summary
    )