from app.models.patient import Patient
from app.models.insurance import Insurance
from app.models.eligibility import Provider


def extract_structured_data(dl_text: str, insurance_text: str):
    """
    Convert OCR text into structured patient and insurance objects.
    """

    # Mock extraction logic for prototype
    patient = Patient(
        first_name="Michael",
        last_name="Motorist",
        dob="1978-03-08",
        gender="M",
        address="345 Anywhere Street, Your City, NY 12345"
    )

    insurance = Insurance(
        payer="UnitedHealthcare",
        member_id="123456789",
        group_number="9999",
        plan_code="UHEALTH",
        rx_bin="610279",
        rx_pcn="9999"
    )

    provider = Provider(
        npi="1234567893",
        organization="iClinic"
    )

    service_date = "2024-01-01"

    return patient, insurance, provider, service_date