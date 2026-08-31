from fastapi import FastAPI, status

app = FastAPI(
    title="Async Log & Alert Processing Engine",
    description="A high-throughput, event-driven backend service for log ingestion and alerting.",
    version="1.0.0"
)

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    """
    Health check endpoint used by load balancers and orchestrators 
    to verify that the service instance is alive and accepting traffic.
    """
    return {
        "status": "healthy",
        "service": "async-log-processor"
    }