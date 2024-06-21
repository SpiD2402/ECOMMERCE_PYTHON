from flask_restx import Resource
from flask import request
from app.schemas.holidays_schema import HolidayRequestSchema
from flask_jwt_extended import jwt_required
from app.controller.holidays_controller import HolidaysController

from app import api

holidays_ns = api.namespace(
    name='Holidays',
    description='Ruta de los Holidays',
    path="/holidays"

)
request_parser =HolidayRequestSchema(holidays_ns)

@holidays_ns.route('')
@holidays_ns.doc(security='Bearer')
class Holidays(Resource):

    @jwt_required()
    @holidays_ns.expect(request_parser.all())
    def get(self):
        '''Listar todos los feriados'''
        query = request_parser.all().parse_args()
        controller = HolidaysController()
        return  controller.all(query);
    @jwt_required()
    @holidays_ns.expect(request_parser.create(), validate=True)
    def post(self):
        '''Crear un Feriado'''
        controller = HolidaysController()
        '''para evitar  traer al request osea imprtar de flask'''
        return controller.create(holidays_ns.payload)

@holidays_ns.route('/<int:id>')
@holidays_ns.doc(security='Bearer')
class HolidaysById(Resource):
    @jwt_required()
    def get(self, id):
        controller = HolidaysController()
        return controller.getById(id)

    @holidays_ns.expect(request_parser.update(), validate=True)
    @jwt_required()
    def put(self, id):
        controller = HolidaysController()
        return controller.update(id, holidays_ns.payload)
    @jwt_required()
    def delete(self, id):
        controller = HolidaysController()
        return controller.delete(id)


@holidays_ns.route('/delivery_dates')
@holidays_ns.doc(security='Bearer')
class DeliveryDates(Resource):
    @jwt_required()
    def get(self):
        '''Listar todas las fecha de entrega disponible'''
        controller= HolidaysController()
        return  controller.deliveryDate()

