from app import db
from app.models.orders_items_model import  OrderItemModel
from app.models.orders_model import OrderModel
from app.utils.mercadopago import  Mercadopago
from app.controller.products_controller import ProductController
from app.controller.coupons_controller import CouponsController
from app.controller.shopping_cart_controller import ShoppingCartController
from flask_jwt_extended import  current_user

class OrdersController:
    def __init__(self):
        self.model = OrderModel
        self.model_item= OrderItemModel
        self.user_id= current_user.id

        self.shopping_cart = ShoppingCartController()
        self.coupon = CouponsController()
        self.product = ProductController()

        self.mercadopago =Mercadopago()


    def create(self,data):
          try:
              coupon =data.get('coupon')
              date_shipping=data.get('date_shipping')
              shopping_cart = self.shopping_cart._getAllProducts(self.user_id)

              products = shopping_cart['data']
              prices = shopping_cart['prices']
              prices['discount']=0
              if not len(products):
                  raise Exception("El carrito de compras esta vacio ")

              if coupon:
                  percentage= self.coupon._validateDateTimeCouponToOrder(coupon)
                  prices['discount']=0 if percentage is None else round(prices['total'] *(percentage/100),2)
                  prices['total']= round(prices['total'] - prices['discount'],2)

              #Creacion del pedido
              order = self.model.create(
                  user_id=self.user_id,
                  total_price=prices['total'],
                  subtotal_price=prices['subtotal'],
                  igv_price=prices['igv'],
                  discount_price =prices['discount'],
                  code_coupon=coupon,
                  date_shipping=date_shipping

              )

              #Creacion del detalle del pedido
              order_items =[
                  self.model_item.create(
                      order_id=order.id,
                      product_id=item['products']['id'],
                      price = item['products']['price'] ,
                      quantity=item['quantity']
                  )
                  for  item in products
              ]

              #Crear la Url de pago
              payment =self.__createPaymentUrl(order,products)
              payment_url= payment['init_point']

              order.checkout_id=payment['id']
              order.checkout_url = payment_url


              #Reducir stock de los productos
              reduces =self.product._reduceStockToProducts(order_items)

              #Limpiar el carrito de compras
              shopping_cart_user=self.shopping_cart._deleteShoppingCartToUser(self.user_id)

              db.session.add(order)
              db.session.add_all(order_items)

              #Guardar o actualizar la reduccion de stock
              db.session.add_all(reduces)

              #Guardar  la limpieza del carrito de compras
              for shop_cart in shopping_cart_user:
                  db.session.delete(shop_cart)

              db.session.commit()
              return {
                    'message':'Se creo el pedido con exito',
                  'data':{
                      'checkout_url': payment_url
                  }
              },200
          except Exception as e:
              db.session.rollback()
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500




    def __createPaymentUrl(self,order,products):
        payer={
            'name':current_user.name,
            'surname':current_user.last_name,
            'email':current_user.email
        }
        items = [
            {
                'id':item['products']['id'],
                'title':item['products']['name'],
                'picture_url':item['products']['image'],
                'quantity':item['quantity'],
                'currency_id':'PEN',
                'unit_price':round(
                    item['products']['price']+(item['products']['price']*self.shopping_cart.igv),
                    2
                )
            }
            for  item in products
        ]
        return self.mercadopago.createPreferences(payer,items,order.id)


