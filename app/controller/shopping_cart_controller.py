from app import  db
from app.models.shopping_cart_model import ShoppingCartModel
from app.schemas.shopping_cart_schemas import ShoppingCartResponseSchema
from flask_jwt_extended import current_user

class ShoppingCartController:
    def __init__(self):
        self.model = ShoppingCartModel
        self.schema = ShoppingCartResponseSchema
        self.user_id =current_user.id
        self.igv=0.18
        self.prices={
            'total':0,
            'subtotal':0,
            'igv':0
        }


    def all(self):
          try:
              return self._getAllProducts(self.user_id),200
          except Exception as e:
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def update(self,data):
          try:
              record = self.model.where(user_id=self.user_id,
                                        product_id=data['product_id']).first()

              if record:
                  record.update(**data)
              else:
                  data['user_id'] = self.user_id
                  record =self.model.create(**data)

              db.session.add(record)
              db.session.commit()
              return {
                  'status': 'ok',
                  'message':'Se actualizo el carritos de compras'
              },200

          except Exception as e:
              db.session.rollback()
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def delete(self,id):
        try:
            record = self.model.where(user_id=self.user_id,
                                      product_id=id).first()
            if record:
                record.delete()
                db.session.commit()
                return {
                    'status': 'ok',
                    'message':'Sele elimino el producto con exito'
                },200

            return {
                'message':'No se encontro el producto mencionado'
            },404

        except Exception as e:
            db.session.rollback()
            return {
                'message' : 'ocurrio un error' ,
                'error' : str(e)
            },200

    def _getAllProducts(self,user_id):
        records = self.model.where(user_id = user_id).all()
        response = self.schema(many = True)
        data = response.dump(records)
        if records :
            for item in data :
                price = item['products']['price']
                quantity = item['quantity']
                self.prices['subtotal'] += price * quantity
        self.prices['igv'] = round(self.prices['subtotal'] * self.igv , 2)
        self.prices['total'] = round(self.prices['subtotal'] + self.prices['igv'] , 2)

        return {
            'data' : data ,
            'prices' : self.prices
        }

    def _deleteShoppingCartToUser(self,user_id):
        records = self.model.where(user_id=user_id).all()
        return  records

