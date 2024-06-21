from  app import api
from flask_restx import  Resource
from app.schemas.products_schemas import ProductRequestSchema
from app.controller.products_controller import  ProductController
from  flask_jwt_extended import  jwt_required

product_ns = api.namespace(
    name='Productos',
    description='Rutas del modelo del Producto',
    path='/products'
)

request_parser =ProductRequestSchema(product_ns)

@product_ns.route('')
@product_ns.doc(security='Bearer')
class Products(Resource):


    @jwt_required()
    @product_ns.expect(request_parser.all())
    def get(self):
        '''Listar todos los Productos'''

        query = request_parser.all().parse_args()
        controller = ProductController()
        return  controller.all(query)

    @jwt_required()
    @product_ns.expect(request_parser.create(),validate=True)
    def post(self):
        '''Crear un Producto'''
        form = request_parser.create().parse_args()
        controller = ProductController()
        return controller.create(form)

@product_ns.route('/<int:id>')
@product_ns.doc(security='Bearer')
class ProductById(Resource):
    def get(self, id):
        '''Retornar un Producto'''
        controller = ProductController()
        return  controller.getById(id)

    @product_ns.expect(request_parser.update(),validate=True)
    def put(self, id):
        '''Modificar un Producto'''
        form = request_parser.update().parse_args()
        controller = ProductController()
        return controller.update(id,form)

    def delete(self, id):
        '''Deletar un Producto'''
        controller = ProductController()
        return  controller.delete(id)
