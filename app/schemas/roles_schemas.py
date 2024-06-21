from flask_restx import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.roles_model import RoleModel
from marshmallow.fields import Nested
from flask_restx.reqparse import RequestParser


class RolesRequestSchema:
    def __init__(self,namespace):
        self.namespace= namespace
    
    def all(self):
        parser =RequestParser()
        parser.add_argument('page',type=int,default =1,location='args')
        parser.add_argument('per_page',type=int,default =5 ,location='args')
        return parser
    
    def create(self):
        return self.namespace.model('Role Create',{
            'name':fields.String(required=True,max_length=80)
        })
    
    def update(self):
        return self.namespace.model('Role Update',{
            'name':fields.String(required=True,max_length=80)
        })
        
        
        
class RolesResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel
        ordered=True

    users=Nested('UsersResponseSchema',exclude=['role'],many=True)

