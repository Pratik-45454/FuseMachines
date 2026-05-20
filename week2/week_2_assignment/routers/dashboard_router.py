# routers/dashboard_router.py
import asyncio
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from logger import get_logger
import crud.customer_crud as customer_crud
# import other cruds as you build them...

logger = get_logger(__name__)
router = APIRouter()

# Individual count endpoints
@router.get("/customers/count")
def customers_count(db: Session = Depends(get_db)):
    logger.info("GET /customers/count")
    count = db.query(__import__('models').Customer).count()
    return {"customers": count}

# The star of Part 3 — concurrent aggregated endpoint
@router.get("/overall_counts")
async def overall_counts(db: Session = Depends(get_db)):
    logger.info("GET /overall_counts - starting all 8 queries concurrently")
    start = time.time()

    async def count_table(model):
        return db.query(model).count()

    import models
    (
        customers, orders, products, employees,
        offices, payments, orderdetails, productlines
    ) = await asyncio.gather(
        asyncio.to_thread(db.query(models.Customer).count),
        asyncio.to_thread(db.query(models.Order).count),
        asyncio.to_thread(db.query(models.Product).count),
        asyncio.to_thread(db.query(models.Employee).count),
        asyncio.to_thread(db.query(models.Office).count),
        asyncio.to_thread(db.query(models.Payment).count),
        asyncio.to_thread(db.query(models.OrderDetail).count),
        asyncio.to_thread(db.query(models.ProductLine).count),
    )

    elapsed = round(time.time() - start, 4)
    logger.info(f"asyncio.gather completed in {elapsed}s")

    return {
        "customers": customers,
        "orders": orders,
        "products": products,
        "employees": employees,
        "offices": offices,
        "payments": payments,
        "orderdetails": orderdetails,
        "productlines": productlines
    }