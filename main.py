from fastapi import FastAPI, status
from schemas import LogPayload, LogIngestResponse

app = FastAPI(
    title="Async Log & Alert Processing Engine",
    description="A high-throughput, event-driven backend service for log ingestion and alerting.",
    version="1.0.0"
)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "async-log-processor"
    }


@app.post(
    "/v1/logs",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=LogIngestResponse,
    tags=["Ingestion"]
)
async def ingest_log(payload: LogPayload):
    """
    Ingest application log events.
    
    Validates the incoming JSON schema and accepts the log payload 
    for non-blocking, asynchronous queue ingestion.
    """
    # Simulate logging the received structured payload
    print(f"[{payload.timestamp}] [{payload.level.value}] [{payload.client_id}]: {payload.message}")
    
    return LogIngestResponse(client_id=payload.client_id)