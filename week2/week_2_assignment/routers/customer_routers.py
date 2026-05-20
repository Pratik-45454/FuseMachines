# routers/customer_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas.customer_schemas as schemas
import crud.customer_crud as crud
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/", response_model=List[schemas.CustomerOut])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"GET /customers - skip={skip}, limit={limit}")
    return crud.get_customers(db, skip=skip, limit=limit)

@router.get("/{customer_number}", response_model=schemas.CustomerOut)
def get_customer(customer_number: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_number}")
    return crud.get_customer(db, customer_number)

@router.post("/", response_model=schemas.CustomerOut)
def create_customer(data: schemas.CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /customers - creating {data.customerNumber}")
    return crud.create_customer(db, data)

@router.put("/{customer_number}", response_model=schemas.CustomerOut)
def update_customer(customer_number: int, data: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /customers/{customer_number}")
    return crud.update_customer(db, customer_number, data)

@router.delete("/{customer_number}")
def delete_customer(customer_number: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /customers/{customer_number}")
    return crud.delete_customer(db, customer_number)

@router.get("/{customer_number}/orders", response_model=List[schemas.OrderOut])
def get_customer_orders(customer_number: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_number}/orders")
    return crud.get_customer_orders(db, customer_number)

@router.get("/{customer_number}/payments", response_model=List[schemas.PaymentOut])
def get_customer_payments(customer_number: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_number}/payments")
    return crud.get_customer_payments(db, customer_number)