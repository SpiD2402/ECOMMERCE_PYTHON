from flask_restx import fields
from flask_restx.reqparse import RequestParser
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.holidays_model import HolidayModel
from marshmallow import  Schema
from  marshmallow.fields import Date,String
class HolidayRequestSchema:
    def __init__(self,namespace):
        self.namespace = namespace

    def all(self):
        parser= RequestParser()
        parser.add_argument('page',type=int,default=1,location='args')
        parser.add_argument('per_page',type=int,default=5,location='args')
        return  parser

    def create(self):
        return self.namespace.model('Holiday Create',{
            'date':fields.Date(required=True),
            'description':fields.String(required=True,max_length = 120)
        })

    def update(self):
        return self.namespace.model('Holiday Update',{
            'date':fields.Date(required=False),
            'description':fields.String(required=False,max_length = 120)
        })

class  HolidayResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =HolidayModel
        ordered = True


class DeliveryDateResponseSchema(Schema):
    date =Date(format = '%Y-%m-%d')
    format=String()