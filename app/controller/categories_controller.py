from app.models.categories_model import CategoryModel
from app.schemas.categories_schema import CategorieResponseSchema
from app import db

class CategoriesController:
    def __init__(self):
        self.model = CategoryModel
        self.schema = CategorieResponseSchema
    def all(self,query):
          try:
              page=query['page']
              per_page=query['per_page']
              records = self.model.where(status=True).order_by('id').paginate(
                  page =page,per_page=per_page

              )
              response = self.schema(many=True)
              return {
                  'results': response.dump(records.items),
                  'pagination':{
                      'totalRecord':records.total,
                      'totalPage':records.pages,
                      'perPage':records.per_page,
                      'currentPage':records.page
                  }
              },200
          except Exception as e:
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def create (self,data):
          try:
              new_record= self.model.create(**data)
              db.session.add(new_record)
              db.session.commit()
              return {
                  'message' : 'Record creado'
              },200
          except Exception as e:
              db.session.rollback()
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
                  'message' : 'Record not found'
              }
          except Exception as e:
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def update(self,id,data):
        try :
            record = self.model.where(id=id).first();
            if record:
                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return {
                    'message' : 'Record modificado'
                },200
            return {
                'message' : 'Record no encontrado'
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
                      'message' : 'Categoria Deshabilitada'
                  },201
              return {
                  'message' : 'Categoria no encontrado'
              },404

          except Exception as e:
              db.session.rollback()
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500