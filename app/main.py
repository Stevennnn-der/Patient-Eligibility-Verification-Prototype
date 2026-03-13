from fastapi import FastAPI
from app.api.routes_documents import router as documents_router
from app.api.routes_eligibility import router as eligibility_router
from app.api.routes_workflow import router as workflow_router

app = FastAPI(
    title="Patient Eligibility Verification Prototype",
    version="1.0.0"
)

app.include_router(documents_router, prefix="/documents", tags=["Documents"])
app.include_router(eligibility_router, prefix="/eligibility", tags=["Eligibility"])
app.include_router(workflow_router, prefix="/workflow", tags=["Workflow"])


@app.get("/")
def root():
    return {"message": "Eligibility prototype is running"}