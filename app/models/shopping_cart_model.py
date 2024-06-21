from app.models.base import BaseModel
from sqlalchemy import Column , Integer,ForeignKey
from sqlalchemy.orm import relationship

class ShoppingCartModel(BaseModel):
    __tablename__ = 'shopping_cart'
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    product_id=Column(Integer,ForeignKey('products.id'))
    quantity=Column(Integer)

    products= relationship('ProductModel', uselist = False,back_populates = 'shopping_carts')
