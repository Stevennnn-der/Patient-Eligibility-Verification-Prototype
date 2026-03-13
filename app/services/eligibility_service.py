from pathlib import Path


def verify_patient_eligibility(data: dict) -> str:
    member_id = data.get("insurance", {}).get("member_id")

    if member_id == "123456789":
        return Path("app/mock/sample_271_active.txt").read_text().strip()

    return Path("app/mock/sample_271_inactive.txt").read_text().strip()