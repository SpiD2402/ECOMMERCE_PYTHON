from sqlalchemy import Column , Integer , String , Text , Float , ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = 'products'
    id=Column(Integer, primary_key=True,autoincrement = True)
    name=Column(String(200))
    description=Column(Text)
    price=Column(Float(precision=2))
    stock=Column(Integer,default=0)
    image=Column(String(255))
    category_id=Column(Integer,ForeignKey('categories.id'))
    status=Column(Boolean,default=True)

    category=relationship('CategoryModel',uselist = False,back_populates = 'products')
    shopping_carts=relationship('ShoppingCartModel',uselist = True,back_populates = 'products')
    order_items = relationship('OrderItemModel',uselist = True,back_populates = 'product')