# Patient Eligibility Verification Prototype

A FastAPI-based prototype for patient insurance eligibility verification. The system accepts identity and insurance documents, extracts structured data, generates a simulated HIPAA 271 response, parses that response, and returns a structured JSON summary for front-desk staff.

This implementation focuses on **clear architecture, API design, validation, and extensibility**, which are the main goals of the assessment.

---

# Overview

The prototype implements three main components:

1. **Document Processing**
  - Accepts a driver's license and insurance card
  - Extracts structured patient and insurance data
2. **Eligibility API Layer**
  - Accepts structured patient and insurance data
  - Returns a simulated HIPAA 271 eligibility response
3. **271 Processing**
  - Parses the 271 response
  - Extracts:
    - coverage status
    - copayment amounts
    - pharmacy information (if present)
  - Returns a structured JSON summary

---

# System Architecture

## High-Level Flow

```text
Uploaded documents
    ↓
Document API
    ↓
OCR service
    ↓
Extraction service
    ↓
Structured patient + insurance data
    ↓
Eligibility API
    ↓
Mock HIPAA 271 response
    ↓
271 parser
    ↓
Structured JSON summary
```

---

# Project Structure

```text
app/
├── main.py
├── api/
│   ├── routes_documents.py
│   ├── routes_eligibility.py
│   └── routes_workflow.py
├── models/
│   ├── patient.py
│   ├── insurance.py
│   └── eligibility.py
├── services/
│   ├── ocr_service.py
│   ├── extraction_service.py
│   ├── eligibility_service.py
│   └── edi271_parser.py
├── mock/
│   ├── sample_271_active.txt
│   └── sample_271_inactive.txt
└── utils/
    └── validators.py
```

---

# Design Logic

## 1. Document Processing

The document processing layer is separated into two services.

### OCR Service

Responsible for reading uploaded files and returning extracted text.

Responsibilities:

- Accept document bytes
- Run OCR or simulated OCR
- Return text content

This layer is isolated so it can later be replaced with:

- Tesseract
- AWS Textract
- Google Vision
- Document AI services

### Extraction Service

Transforms OCR text into structured domain objects.

Structured outputs include:

- Patient information
- Insurance information
- Provider information
- Service date

This separation ensures the system remains modular and easy to extend.

---

## 2. Eligibility API Layer

The eligibility API accepts structured patient and insurance data and returns a simulated HIPAA 271 response.

The system uses **mock 271 responses** instead of a live payer or clearinghouse integration.

This design keeps the prototype deterministic and easy to test while still demonstrating the required eligibility workflow.

Example logic:

- Known member ID → active coverage response
- Unknown member ID → inactive coverage response

---

## 3. 271 Processing

The 271 parser reads raw EDI text and converts it into structured data.

The parser processes key EDI segments:


| Segment | Purpose                          |
| ------- | -------------------------------- |
| NM1     | Payer and member identification  |
| DTP     | Service date                     |
| EB      | Coverage and benefit information |
| REF     | Pharmacy and plan references     |


The parser extracts:

- coverage status
- copayment amounts
- pharmacy BIN and PCN

These values are returned as a **structured JSON summary** suitable for front-desk staff instead of raw EDI.

---

# API Endpoints

## Document Extraction

`POST /documents/extract`

Uploads documents and returns structured data.

Response includes:

- patient
- insurance
- provider
- service date
- warnings

---

## Eligibility Verification

`POST /eligibility/verify`

Accepts structured patient and insurance data and returns:

- raw 271 response
- parsed eligibility summary

---

## Parse 271

`POST /eligibility/parse`

Accepts a raw 271 message and returns a parsed summary.

This endpoint allows the parser to be used independently.

---

## Full Workflow

`POST /workflow/eligibility-check`

Runs the entire process:

1. Upload documents
2. Extract structured data
3. Verify eligibility
4. Parse 271 response
5. Return final summary

This endpoint demonstrates the full system workflow.

---

# Validation and Error Handling

The system includes validation at several stages.

## File Validation

Supported file types:

- image/jpeg
- image/png
- application/pdf

Unsupported file types return:

`400 Bad Request`

---

## Request Validation

Eligibility requests validate:

- presence of member ID
- valid NPI format
- valid service date format (YYYY-MM-DD)

Invalid input returns:

`422 Unprocessable Entity`

---

## 271 Parsing Safety

The parser handles:

- empty EDI responses
- malformed 271 messages

Errors return safe client-facing responses instead of crashing the service.

---

# Key Design Decisions

## FastAPI

FastAPI was chosen because it provides:

- automatic API documentation
- strong request validation
- simple development workflow
- clean backend architecture

---

## Mock Eligibility Responses

Real eligibility verification typically requires clearinghouse integration and payer connectivity.

For this prototype, mock 271 responses are used to demonstrate the eligibility workflow without external dependencies.

---

## Modular Service Design

The system separates responsibilities into services:

- OCR
- extraction
- eligibility verification
- EDI parsing

This structure improves:

- maintainability
- extensibility
- testability

---

# Trade-offs

This prototype intentionally makes several trade-offs.

### Prototype OCR

The OCR layer is simplified and does not attempt to support all real-world document formats.

### Mock Eligibility

Eligibility verification uses stored responses rather than real payer integrations.

### Simplified EDI Parsing

The parser focuses only on fields required by the assessment rather than implementing a full EDI interpreter.

These trade-offs allow the system to demonstrate architecture and workflow clearly.

---

# Limitations

Current limitations include:

- OCR is simulated
- extraction logic is simplified
- only a subset of 271 segments are parsed
- no real clearinghouse integration
- no authentication or access control

---

# Potential Production Improvements

A production version could include:

- real OCR or document AI
- confidence scoring for extraction
- support for multiple insurance card formats
- clearinghouse integration
- expanded 271 parsing logic
- authentication and authorization
- encrypted document storage
- audit logging

---

# Running the Project

## Install Dependencies

```{bash}
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start the Server

```{bash}
uvicorn app.main:app --reload
```

## Open API Docs

```{bash}
http://127.0.0.1:8000/docs
```

---

# Demo Flow

A recommended demo sequence:

1. Upload documents using `/documents/extract`
2. Show extracted patient and insurance data
3. Call `/eligibility/verify`
4. Show raw 271 response
5. Show parsed JSON summary
6. Demonstrate `/workflow/eligibility-check` for the full pipeline

---

# Summary

This prototype demonstrates a complete eligibility verification workflow with:

- modular architecture
- clear API design
- structured data extraction
- simulated eligibility verification
- practical HIPAA 271 parsing
- useful JSON output for front-desk use

The system emphasizes clarity, extensibility, and maintainability while meeting the functional requirements of the assessment.