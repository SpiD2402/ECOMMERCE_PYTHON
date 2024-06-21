from app import  db
from app.models.products_model import  ProductModel
from app.utils.bucket import  Bucket
from app.schemas.products_schemas import ProductResponseSchema
from sqlalchemy import  or_

class ProductController:
    def __init__(self):
        self.model = ProductModel
        self.bucket = Bucket('ecommerce-spid','products')
        self.schema = ProductResponseSchema
        self.__allowed_extensions=['jpg','jpeg','png','webp']

    def all(self,query):
          try:
              filters ={}
              page = query.get('page')
              per_page = query.get('per_page')

              if query['q']:
                  filters={
                        or_:{
                            'name__ilike':f"%{query['q']}%",
                            'description__ilike':f"%{query['q']}%",
                        }
                  }

              if query['category_id']:
                  filters['category_id'] = query['category_id']

              if query['status'] is not  None:
                  filters['status'] = bool(query['status'])


              ordering = query['ordering'].split(',') if query['ordering'] else ['id']
              print(ordering)


              #records = self.model.where(status=True).order_by('id').paginate(
              #    page=page,per_page=per_page,
              #)

              records=self.model.smart_query(
                    filters={**filters},
                    sort_attrs = ordering
              ).paginate(
                  page=page,per_page=per_page
              )

              response =self.schema(many=True)
              return {
                  'results':response.dump(records.items),
                  'paginaton':{
                      'totalRecords':records.total,
                      'totalPages':records.pages,
                      'perPage':records.per_page,
                      'currentPage':records.page,
                  }
              },200

          except Exception as e:
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500


    def getById(self,id):
          try:
              record= self.model.where(id=id).first()
              response = self.schema(many=False)
              if record:
                  return{
                      'data':response.dump(record)
                  },200
              return {
                  'message' : 'No se encontro el producto mencionado'
              }
          except Exception as e:
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500



    def create(self,data):
        try:
            image = data.get('image')
            filename,stream=self.__validateExtensionImage(image)
            image_url=self.bucket.uploadObject(filename,stream)
            data['image']=image_url
            new_record= self.model.create(**data)
            db.session.add(new_record)
            db.session.commit()
            return {
                    'status':'ok',
                    'message':f'El producto {data["name"]} se a creado con exito'
            },200
        except Exception as e:
            db.session.rollback()
            return {
                'message' : 'ocurrio un error' ,
                'error' : str(e)
            } , 500


    def update(self,id,data):
        try :

            record = self.model.where(id = id).first();
            if record :
                image = data.get('image')
                if image:
                    filename , stream = self.__validateExtensionImage(image)
                    image_url = self.bucket.uploadObject(filename , stream)
                    data['image'] = image_url

                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return {
                    'message' : f'El producto con el  {id} a sido modificado'
                } , 200
            return {
                'message' : 'Producto no encontrado'
            } , 404
        except Exception as e :
            db.session.rollback()
            return {
                'message' : 'ocurrio un error' ,
                'error' : str(e)
            } , 500


    def delete(self,id):
          try:
              record = self.model.where(id=id).first()
              if record and record.status:
                  record.update(status=False)
                  db.session.add(record)
                  db.session.commit()
                  return {
                      'message' : 'Producto Deshabilitado'
                  },201
              return {
                  'message' : 'Producto no encontrado'
              },404

          except Exception as e:
              db.session.rollback()
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def __validateExtensionImage(self,obj_image):
        filename = obj_image.filename
        stream = obj_image.stream
        extension=filename.split('.')[1]
        if extension not in self.__allowed_extensions:
            raise Exception('El tipo de archivo usado, no esta permitido')

        return  filename,stream


    def _reduceStockToProducts(self,items):
        updates =[]
        for item in items:
            record= self.model.where(id=item.product_id).first()
            new_stock = record.stock - item.quantity
            record.update(stock=new_stock)
            updates.append(record)

        return updates








