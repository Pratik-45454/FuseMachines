from fastapi import FastAPI
from routers.customer_router import router as customer_router
from database import engine, Base
from logger import get_logger

logger = get_logger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClassicModels API", version="1.0")

app.include_router(customer_router, prefix="/customers", tags=["Customers"])
@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "ClassicModels API is running!"}