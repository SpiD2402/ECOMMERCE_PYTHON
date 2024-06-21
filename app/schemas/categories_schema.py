from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_restx import fields
from flask_restx.reqparse import RequestParser
from app.models.categories_model import CategoryModel

class CategorieSchema:
    def __init__(self,namespace):
        self.namespace = namespace

    def all(self):
        parser= RequestParser()
        parser.add_argument('page',type=int,default=1,location='args')
        parser.add_argument('per_page',type=int,default=5,location='args')
        return  parser

    def create(self):
        return self.namespace.model('Categoria Create',{
            'name':fields.String(required=True,max_length = 80,min_length = 5)
        })

    def update(self):
        return self.namespace.model('Categoria Update',{
            'name':fields.String(required=False,max_length = 80,min_length = 5)
        })


class CategorieResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        ordered = True