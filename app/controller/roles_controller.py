from app.models.roles_model import RoleModel
from app.schemas.roles_schemas import RolesResponseSchema

from  app import db

class RoleController:
    def  __init__(self):
      self.model = RoleModel
      self.schema= RolesResponseSchema
    
    def all(self,query):
        try:
            #Pagiante
            '''
            page -> Pagina actual
            per_page ->Total de registro por pagina
            total -> total de registros
            pages -> total de paginas
            item -> Lista de objetos
            
            '''
            
            page =query['page']
            per_page=query['per_page']
            records = self.model.where(status=True).order_by('id').paginate(
                page=page,per_page=per_page

            )
            response = self.schema(many=True)
            
            return {
                'results':response.dump(records.items),
                'pagination':{
                    'totalRecords':records.total,
                    'totalPages':records.pages,
                    'perPage':records.per_page,
                    'currentPage':records.page                    
                }
                
            }, 200
        
        except Exception as e:
            return{
                "error":"error"
            },500
        
    def getById(self,id):
        
        try:
            record = self.model.where(id=id).first()
            response =  self.schema(many=False)
            if record:
                return{
                        'data':response.dump(record)
                },200
            return {
                'message':'No se encontro el rol mencionado'
            },404
                
        except Exception as e:
            return{
                "message":"Ocurrio un Error",
                'error':str(e)
            },500
             
      
    
    def create(self,data):
        try:
            new_record = self.model.create(**data)
            db.session.add(new_record)
            db.session.commit()
            
            return{
                'data': f"El rol {data["name"]} se a creado con exito"
            },201
            
            
        except Exception  as e:
            db.session.rollback()
            return{
                "message":"Ocurrio un Error",
                'error':str(e)
            },500
             
            
    def update(self,id,data):
        try:
            record= self.model.where(id = id).first()
            if record:
                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return{
                    'message':'El rol {id}, ha sido actualizado'
                },200
                
            return {
                'message':'No se encontro el rol mencionado'
            },404
        except Exception as e:
            db.session.rollback()
            return{
                'message':"Ocurrio un error",
                'error':str(e)
                
            },500
    def delete (self,id):
        try:
            record = self.model.where(id=id).first()
            if(record  and record.status):
                record.update(status =False)
                db.session.add(record)
                db.session.commit()
                return{
                    'message':'El rol {id}, ha sido deshabilitado'
                },200
            return {
                'message':'No se encontro el rol mencionado'
            },404
        except Exception as e:
            db.session.rollback()
            return{
                'message':"Ocurrio un error",
                'error':str(e)
                },500