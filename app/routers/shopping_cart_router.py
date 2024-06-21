from app import api
from flask_restx import Resource
from flask_jwt_extended import  jwt_required
from app.schemas.shopping_cart_schemas import ShoppingCartRequestSchema
from app.controller.shopping_cart_controller import  ShoppingCartController

shopping_ns = api.namespace(

    name='Shopping Cart',
    description='Shopping Cart Router',
    path='/shopping_cart'
)

request_schema = ShoppingCartRequestSchema(shopping_ns)


@shopping_ns.route('')
@shopping_ns.doc(security='Bearer')
class ShoppingCart(Resource):

    @jwt_required()
    def get(self):
        '''Listar los productos del carrito'''
        controller =ShoppingCartController()
        return controller.all()
    @jwt_required()
    @shopping_ns.expect(request_schema.update(), validate=True)
    def put(self):
        '''Crear o actualizar  un producto en el carrito'''
        controller = ShoppingCartController()
        return controller.update(shopping_ns.payload)

@shopping_ns.route('/<int:product_id>')
@shopping_ns.doc(security='Bearer')
class ShoppingCartByProductId(Resource):
    @jwt_required()
    def delete(self, product_id):
        '''Eliminar un producto en el carrito'''
        controller = ShoppingCartController()
        return controller.delete(product_id)