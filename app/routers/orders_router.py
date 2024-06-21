from app import  api
from flask_restx import Resource
from flask_jwt_extended import  jwt_required
from app.schemas.orders_schemas import  OrderRequestSchema
from app.controller.orders_controller import OrdersController


order_ns = api.namespace(
    name='Ordenes de compra',
    description='Ruta para el modelo de ordenes',
    path='/orders'

)

request_schema=OrderRequestSchema(order_ns)

@order_ns.route('')
@order_ns.doc(security='Bearer')
class Order(Resource):

    @jwt_required()
    @order_ns.expect(request_schema.create(), validate=True)
    def post(self):
        '''Creacion de un pedido'''
        controller = OrdersController()
        return controller.create(order_ns.payload)