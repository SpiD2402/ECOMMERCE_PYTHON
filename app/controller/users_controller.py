from app.models.users_model import UserModel
from app.schemas.users_schemas import UsersResponseSchema
from flask_jwt_extended import current_user
from app import db


class UsersController :
    def __init__(self) :
        self.model = UserModel
        self.schema = UsersResponseSchema
        self.current_user=current_user

    def all(self , query) :
        try :
            page = query['page']
            per_page = query['per_page']
            records = self.model.where(status = True).order_by('id').paginate(
                page = page , per_page = per_page ,
            )
            response = self.schema(many = True)

            return {
                'results' : response.dump(records.items) ,
                'pagination' : {
                    'totalRecords' : records.total ,
                    'totalPages' : records.pages ,
                    'perPage' : records.per_page ,
                    'currentPage' : records.page ,
                }
            } , 200

        except Exception as e :
            return {
                'message' : 'ocurrio un error' ,
                'error' : str(e)
            },500

    def getById(self , id):
        try:
            record= self.model.where(id = id,status =True ).first()
            response= self.schema(many = False)
            if record:
                return {
                    'data':response.dump(record)
                },200
            return {
                'message' : 'no existe el usuario',
            }

        except Exception as e :
            return {
                'message' : 'ocurrio un error' ,
                'error' : str(e)
            } , 500


    def create(self , data) :
        try:
            new_record = self.model.create(**data)
            new_record.hashPassword()
            db.session.add(new_record)
            db.session.commit()
            return{
                'message': 'Se creo con exito el Usuario',
            },201
        except Exception as e:
            db.session.rollback()
            return {
                'message' : 'ocurrio un error' ,
                'error' : str(e)
            },500

    def update(self,id,data):
        try:
            record = self.model.where(id = id,status = True ).first()
            if record:
                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return {
                    'message' : f'Se actualiza con exito el Usuario con el id {id}',
                },200
            return {
                'message' : 'no existe el usuario' ,
            },404
        except Exception as e :
            db.session.rollback()
            return {
                'message' : 'ocurrio un error' ,
                'error' : str(e)
            } , 500

    def delete(self , id):
        try:
            record = self.model.where(id = id).first()
            if record and record.status:
                record.status = False
                db.session.add(record)
                db.session.commit()
                return {
                    'message' : 'Se deshabilito el usuario',
                },200
            return {
                'message' : 'El usuario no existe o ya fue deshabilitado',
            }
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'ocurrio un error',
                'error': str(e)
            },500

    def profileMe(self):
        try:
            user_id=self.current_user.id
            record = self.model.where(id = user_id , status = True).first()
            if record :
                response = self.schema(many = False)
                return {
                    'data' : response.dump(record)
                } , 200
            return {
                'message' : 'no existe el usuario' ,
            }


        except Exception as e:
            return {
                'message': 'ocurrio un error',
                'error': str(e)
            },500