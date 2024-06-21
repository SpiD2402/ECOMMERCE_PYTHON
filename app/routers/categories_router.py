from flask_restx import Resource
from flask import request
from app.schemas.categories_schema import CategorieSchema
from flask_jwt_extended import jwt_required
from app.controller.categories_controller import CategoriesController
from app import api

categories_ns = api.namespace(
    name='Categories',
    description='Ruta de las categories',
    path="/categories"

)

request_schema =CategorieSchema(categories_ns)

@categories_ns.route('')
@categories_ns.doc(security='Bearer')
class Categories(Resource):

    @jwt_required()
    @categories_ns.expect(request_schema.all())
    def get(self):
        query = request_schema.all().parse_args()
        controller = CategoriesController()
        return controller.all(query)

    @categories_ns.expect(request_schema.create(), validate=True)
    @jwt_required()
    def post(self):
        controller = CategoriesController()
        return  controller.create(request.json)

@categories_ns.route('/<int:id>')
@categories_ns.doc(security='Bearer')
class CategoriesById(Resource):
    @jwt_required()
    def get(self, id):
        controller = CategoriesController()
        return  controller.getById(id)
    @categories_ns.expect(request_schema.update(), validate=True)
    @jwt_required()
    def put(self, id):
        controller = CategoriesController()
        return controller.update(id, request.json)

    @jwt_required()
    def delete(self, id):
        controller = CategoriesController()
        return  controller.delete(id)