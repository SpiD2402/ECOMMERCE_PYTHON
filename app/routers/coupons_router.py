from flask import request
from flask_restx import Resource
from app.controller.coupons_controller import CouponsController
from app.schemas.coupons_schema import CouponSchema
from flask_jwt_extended import jwt_required

from app import api

coupons_ns = api.namespace(
    name='Coupons',
    description='Ruta de los cupones',
    path="/coupons"

)

request_schema=CouponSchema(coupons_ns)

@coupons_ns.route('')
@coupons_ns.doc(security='Bearer')
class Coupons(Resource):

    @jwt_required()
    @coupons_ns.expect(request_schema.all())
    def get(self):
        query = request_schema.all().parse_args()
        controller= CouponsController()
        return  controller.all(query)
    @jwt_required()
    @coupons_ns.expect(request_schema.create())
    def post(self):
        controller= CouponsController()
        return controller.create(request.json)
@coupons_ns.route('/<int:id>')
@coupons_ns.doc(security='Bearer')
class CouponsById(Resource):
    @jwt_required()
    def get(self, id):
        controller= CouponsController()
        return  controller.getById(id)

    @coupons_ns.expect(request_schema.update())
    @jwt_required()
    def put(self, id):
        controller = CouponsController()
        return controller.update(id,request.json)
    @jwt_required()
    def delete(self, id):
        controller = CouponsController()
        return controller.delete(id)


@coupons_ns.route('/validate/<code>')
@coupons_ns.doc(security='Bearer')
class CouponsByCode(Resource):
    @jwt_required()
    def get(self, code):
        '''Obtener un cupon por el code'''
        controller= CouponsController()
        return  controller.validate(code)