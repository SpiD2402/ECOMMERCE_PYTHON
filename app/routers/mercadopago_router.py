from app import  api
from flask import  request
from flask_restx import  Resource
from app.schemas.mercadopago_schemas import  MercadopagoRequestSchema
from  app.utils.mercadopago import  Mercadopago
from app.controller.mercadopago_controller import MercadopagoController


mercadopago_ns = api.namespace(
    name='Mercadopago',
    description='Rutas para la integracion con Mercado Pago',
    path='/mercadopago'
)

request_schema = MercadopagoRequestSchema(mercadopago_ns)

@mercadopago_ns.route('/users/test')
class UserTest(Resource):

    @mercadopago_ns.expect(request_schema.createUserTest(),validate=True)
    def post(self):
        '''crear usuario de prueba'''
        mercadopago= Mercadopago()
        return mercadopago.createUserTest(mercadopago_ns.payload)


@mercadopago_ns.route('/webhook')
class Webhook(Resource):
    def post(self):
        '''Recepcion de pagos '''
        query= request.args.to_dict()
        payment_id=query['id']
        controller = MercadopagoController()
        controller.updatePaymentStatus(payment_id)
        return {},200







