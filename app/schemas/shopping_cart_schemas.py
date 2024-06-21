from flask_restx import  fields
from  marshmallow_sqlalchemy import  SQLAlchemyAutoSchema
from app.models.shopping_cart_model import  ShoppingCartModel
from marshmallow.fields import Nested

class ShoppingCartRequestSchema:
    def __init__(self,namespace):
        self.namespace = namespace

    def update(self):
        return self.namespace.model('Shopping Cart CreateOrUpdate',{

            'product_id':fields.Integer(required=True),
            'quantity':fields.Integer(required=True,min = 1)
        })



class ShoppingCartResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShoppingCartModel
        ordered = True

    products =Nested('ProductResponseSchema',many = False)