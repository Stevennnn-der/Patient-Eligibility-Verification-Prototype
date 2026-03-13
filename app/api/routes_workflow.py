from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.eligibility import (
    ExtractionResponse,
    EligibilityRequest,
    EligibilityResponse,
    WorkflowEligibilityResponse,
)
from app.services.ocr_service import extract_text_from_image
from app.services.extraction_service import extract_structured_data
from app.services.eligibility_service import verify_patient_eligibility
from app.services.edi271_parser import parse_271_message
from app.utils.validators import is_valid_npi, is_valid_date

router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}


def validate_file(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}"
        )


@router.post("/eligibility-check", response_model=WorkflowEligibilityResponse)
async def run_eligibility_check(
    drivers_license: UploadFile = File(...),
    insurance_card: UploadFile = File(...)
):
    validate_file(drivers_license)
    validate_file(insurance_card)

    dl_bytes = await drivers_license.read()
    ins_bytes = await insurance_card.read()

    # OCR
    dl_text = extract_text_from_image(dl_bytes)
    insurance_text = extract_text_from_image(ins_bytes)

    # Extraction
    patient, insurance, provider, service_date = extract_structured_data(
        dl_text,
        insurance_text
    )

    extracted_data = ExtractionResponse(
        patient=patient,
        insurance=insurance,
        provider=provider,
        service_date=service_date,
        warnings=[]
    )

    # Validation
    if not insurance.member_id:
        raise HTTPException(status_code=422, detail="insurance.member_id is required")

    if not is_valid_npi(provider.npi):
        raise HTTPException(status_code=422, detail="provider.npi must be 10 digits")

    if not is_valid_date(service_date):
        raise HTTPException(status_code=422, detail="service_date must be YYYY-MM-DD")

    # Build eligibility request
    eligibility_request = EligibilityRequest(
        patient=patient,
        insurance=insurance,
        provider=provider,
        service_date=service_date,
    )

    # Verify + parse
    raw_271 = verify_patient_eligibility(eligibility_request.model_dump())
    summary = parse_271_message(raw_271)

    eligibility_result = EligibilityResponse(
        raw_271=raw_271,
        summary=summary
    )

    return WorkflowEligibilityResponse(
        extracted_data=extracted_data,
        eligibility_result=eligibility_result
    )