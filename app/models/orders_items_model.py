from sqlalchemy import Column , Integer,Float,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import  BaseModel


class OrderItemModel(BaseModel):
    __tablename__ = 'orders_items'
    id=Column(Integer, primary_key=True, autoincrement=True)
    order_id=Column(Integer,ForeignKey('orders.id'))
    product_id=Column(Integer, ForeignKey('products.id'))
    price=Column(Float(precision = 2))
    quantity=Column(Integer)

    order =relationship('OrderModel',uselist = False,back_populates = 'items')
    product   = relationship('ProductModel',uselist = False,back_populates = 'order_items')