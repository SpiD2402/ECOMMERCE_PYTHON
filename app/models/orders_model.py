from sqlalchemy import Column , Integer , ForeignKey,Float,String,Date
from sqlalchemy.orm import  relationship
from app.models.base import  BaseModel
from sqlalchemy.sql import  func



class OrderModel(BaseModel):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id=Column(Integer, ForeignKey('users.id'))
    total_price=Column(Float(precision = 2))
    subtotal_price=Column(Float(precision = 2))
    igv_price=Column(Float(precision = 2))
    discount_price=Column(Float(precision = 2))
    code_coupon=Column(String(50),nullable=True)
    date_create=Column(Date,default=func.now())
    date_shipping=Column(Date)


    checkout_id=Column(String(255),nullable=True)
    checkout_url=Column(String(255),nullable=True)
    payment_status =Column(String(255),nullable=True)
    payment_detail=Column(String(255),nullable=True)



    status=Column(String,default='pending')
    items =relationship('OrderItemModel',uselist = True,back_populates = 'order')
