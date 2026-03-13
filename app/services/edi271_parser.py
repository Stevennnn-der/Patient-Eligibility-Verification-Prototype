from typing import Optional
from app.models.eligibility import (
    EligibilitySummary,
    CopaySummary,
    PharmacySummary,
)


def format_yyyymmdd(raw_date: str) -> Optional[str]:
    """
    Convert YYYYMMDD -> YYYY-MM-DD
    """
    if not raw_date or len(raw_date) != 8 or not raw_date.isdigit():
        return None
    return f"{raw_date[0:4]}-{raw_date[4:6]}-{raw_date[6:8]}"


def safe_float(value: str):
    """
    Convert a string to float when possible.
    Returns None if conversion fails.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_271_message(raw_271: str) -> EligibilitySummary:
    """
    Parse a raw 271 EDI message into a business-friendly EligibilitySummary.
    """

    if not raw_271 or not raw_271.strip():
        raise ValueError("Empty 271 message")

    try:
        segments = [segment.strip() for segment in raw_271.split("~") if segment.strip()]
    except Exception as exc:
        raise ValueError("Malformed 271 format") from exc

    payer = None
    member_id = None
    service_date = None

    coverage_active = False

    general_visit = None
    specialist_visit = None
    emergency_visit = None
    deductible = None

    pharmacy_enabled = False
    rx_bin = None
    rx_pcn = None

    eb_amounts = []

    for segment in segments:
        elements = segment.split("*")
        if not elements:
            continue

        tag = elements[0]

        if tag == "NM1":
            if len(elements) > 3 and elements[1] == "PR":
                payer = elements[3]

            if len(elements) > 9 and elements[1] == "IL":
                member_id = elements[9]

        elif tag == "DTP":
            if len(elements) > 3 and elements[1] == "291":
                parsed_date = format_yyyymmdd(elements[3])
                if parsed_date:
                    service_date = parsed_date

        elif tag == "EB":
            if len(elements) > 1 and elements[1] == "1":
                coverage_active = True
            elif len(elements) > 1 and elements[1] == "6":
                coverage_active = False

            if len(elements) > 3 and elements[3] == "88":
                pharmacy_enabled = True

            if len(elements) > 5 and elements[5]:
                amount = safe_float(elements[5])
                if amount is not None:
                    eb_amounts.append(amount)

        elif tag == "REF":
            if len(elements) > 2:
                qualifier = elements[1]
                value = elements[2]

                if qualifier == "6P":
                    rx_bin = value
                elif qualifier == "HJ":
                    rx_pcn = value

    if len(eb_amounts) > 0:
        general_visit = eb_amounts[0]
    if len(eb_amounts) > 1:
        specialist_visit = eb_amounts[1]
    if len(eb_amounts) > 2:
        emergency_visit = eb_amounts[2]
    if len(eb_amounts) > 3:
        deductible = eb_amounts[3]

    return EligibilitySummary(
        coverage_active=coverage_active,
        payer=payer,
        member_id=member_id,
        service_date=service_date,
        copay=CopaySummary(
            general_visit=general_visit,
            specialist_visit=specialist_visit,
            emergency_visit=emergency_visit,
            deductible=deductible,
        ),
        pharmacy=PharmacySummary(
            enabled=pharmacy_enabled,
            rx_bin=rx_bin,
            rx_pcn=rx_pcn,
        ),
        raw_271_reference="parsed-from-raw",
    )