from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.eligibility import ExtractionResponse
from app.services.ocr_service import extract_text_from_image
from app.services.extraction_service import extract_structured_data

router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}


def validate_file(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}"
        )


@router.post("/extract", response_model=ExtractionResponse)
async def extract_documents(
    drivers_license: UploadFile = File(...),
    insurance_card: UploadFile = File(...)
):
    validate_file(drivers_license)
    validate_file(insurance_card)

    dl_bytes = await drivers_license.read()
    ins_bytes = await insurance_card.read()

    dl_text = extract_text_from_image(dl_bytes)
    insurance_text = extract_text_from_image(ins_bytes)

    patient, insurance, provider, service_date = extract_structured_data(
        dl_text,
        insurance_text
    )

    return ExtractionResponse(
        patient=patient,
        insurance=insurance,
        provider=provider,
        service_date=service_date,
        warnings=[]
    )