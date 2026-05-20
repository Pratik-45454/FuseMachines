# schemas/customer_schemas.py
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
import datetime

class OrderOut(BaseModel):
    orderNumber: int
    orderDate: datetime.date
    requiredDate: datetime.date
    shippedDate: Optional[datetime.date] = None
    status: str
    comments: Optional[str] = None
    customerNumber: int

    class Config:
        from_attributes = True

class PaymentOut(BaseModel):
    customerNumber: int
    checkNumber: str
    paymentDate: datetime.date
    amount: Decimal

    class Config:
        from_attributes = True

class CustomerCreate(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

class CustomerOut(CustomerCreate):
    orders: List[OrderOut] = []
    payments: List[PaymentOut] = []

    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None