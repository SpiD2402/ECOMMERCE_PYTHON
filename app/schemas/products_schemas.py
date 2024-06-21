from flask_restx.reqparse import  RequestParser
from werkzeug.datastructures import FileStorage
from marshmallow_sqlalchemy import  SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from app.models.products_model import ProductModel

class ProductRequestSchema:
    def __init__(self,namespace):
        self.namespace= namespace


    def all(self):
        parser = RequestParser()
        parser.add_argument('page',type=int,default=1,location='args')
        parser.add_argument('per_page' , type = int , default = 5 , location = 'args')
        parser.add_argument('q',type=str,location = 'args',required = False)
        parser.add_argument('category_id',type=int,required = False,location = 'args')
        parser.add_argument('status',type=int,required=False,location = 'args')
        parser.add_argument('ordering',type=str,required = False,location = 'args')
        return  parser

    def create(self):
        parser = RequestParser()
        parser.add_argument('name',type=str,required=True,location='form')
        parser.add_argument('description',type=str,required=True,location='form')
        parser.add_argument('price',type=float,required=True,location='form')
        parser.add_argument('stock' , type = int , required = True , location = 'form')
        parser.add_argument('image',type=FileStorage, required = True , location = 'files')
        parser.add_argument('category_id',type = int , required = True , location = 'form')

        return  parser


    def update(self):
        parser = RequestParser()
        parser.add_argument('name',type=str,required=False,location='form')
        parser.add_argument('description',type=str,required=False,location='form')
        parser.add_argument('price',type=float,required=False,location='form')
        parser.add_argument('stock' , type = int , required = False , location = 'form')
        parser.add_argument('image',type=FileStorage, required = False , location = 'files')
        parser.add_argument('category_id',type = int , required = False , location = 'form')

        return  parser

class ProductResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        ordered = True

    category=Nested('CategorieResponseSchema',many = False)
