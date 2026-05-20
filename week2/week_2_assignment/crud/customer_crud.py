# crud/customer_crud.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas.customer_schemas as schemas
from logger import get_logger

logger = get_logger(__name__)

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching customers: skip={skip}, limit={limit}")
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_number: int):
    logger.info(f"Fetching customer: {customer_number}")
    customer = db.query(models.Customer).filter(
        models.Customer.customerNumber == customer_number
    ).first()
    if not customer:
        logger.warning(f"Customer not found: {customer_number}")
        raise HTTPException(status_code=404, detail=f"Customer {customer_number} not found")
    return customer

def create_customer(db: Session, data: schemas.CustomerCreate):
    logger.info(f"Creating customer: {data.customerNumber}")
    customer = models.Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    logger.info(f"Customer created: {customer.customerNumber}")
    return customer

def update_customer(db: Session, customer_number: int, data: schemas.CustomerUpdate):
    logger.info(f"Updating customer: {customer_number}")
    customer = get_customer(db, customer_number)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    logger.info(f"Customer updated: {customer_number}")
    return customer

def delete_customer(db: Session, customer_number: int):
    logger.info(f"Deleting customer: {customer_number}")
    customer = get_customer(db, customer_number)
    db.delete(customer)
    db.commit()
    logger.info(f"Customer deleted: {customer_number}")
    return {"message": f"Customer {customer_number} deleted"}

def get_customer_orders(db: Session, customer_number: int):
    logger.info(f"Fetching orders for customer: {customer_number}")
    customer = get_customer(db, customer_number)
    return customer.orders

def get_customer_payments(db: Session, customer_number: int):
    logger.info(f"Fetching payments for customer: {customer_number}")
    customer = get_customer(db, customer_number)
    return customer.payments

# In each crud file, add a count function
def get_customers_count(db: Session) -> int:
    logger.info("Counting customers")
    return db.query(models.Customer).count()