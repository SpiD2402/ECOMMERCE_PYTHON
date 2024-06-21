from app import api
from flask import request
from flask_restx import Resource
from app.schemas.roles_schemas import RolesRequestSchema
from app.controller.roles_controller import RoleController
from flask_jwt_extended import jwt_required 

role_ns = api.namespace(
    
    name='Roles',
    description='Rutas del modelo de Roles',
    path='/roles'
    
)

request_schema = RolesRequestSchema(role_ns);



@role_ns.route('')
@role_ns.doc(security='Bearer')
class Roles(Resource):
    
    @jwt_required()
    @role_ns.expect(request_schema.all())
    def get(self):
        ''' Listar Todos los Roles'''
        query = request_schema.all().parse_args()
        controller = RoleController()
        return controller.all(query)

    @jwt_required()
    @role_ns.expect(request_schema.create(),validate=True)    
    def post(self):
        '''Crear los Roles'''    
        controller = RoleController()
        return controller.create(request.json)
    
@role_ns.route('/<int:id>')
@role_ns.doc(security='Bearer')
class RolesById(Resource):
    
    @jwt_required()
    def get(self,id):
        '''Obtener un ROL  por el ID'''
        controller = RoleController()
        return controller.getById(id)
   
    @jwt_required()
    @role_ns.expect(request_schema.update(),validate=True)      
    def put(self,id):
        '''Actualizar un por el ID'''
        controller = RoleController()
        return controller.update(id,request.json)
        
    @jwt_required()
    def delete(self,id):
        '''Deshabilitar un rol por el ID'''
        controller = RoleController()
        return controller.delete(id)    
