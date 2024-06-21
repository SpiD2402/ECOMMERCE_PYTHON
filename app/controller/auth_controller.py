from app import db
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token,create_refresh_token
from  secrets import  token_hex
from app.utils.mailing import Mailing

class AuthController:
    def __init__(self):
        self.model = UserModel
        self.rol_id = 2
        self.mailing = Mailing()
    
    def signUp(self,data):
        try:
            data['rol_id']=self.rol_id
            new_record=self.model.create(**data)
            new_record.hashPassword()
            db.session.add(new_record)
            db.session.commit()

            return{
                'message':'Creacion Exitosa del Usuario',
            },201
            
        except Exception as e:
            db.session.rollback()
            return{
                "message":"Ocurrio un Error",
                'error':str(e)
            },500
    def signIn(self,data):
        try:
            username = data['username']
            password= data['password']
            
            #Validar usuario
            record = self.model.where(username=username,status=True).first()
            if record:
                if record.checkPassword(password):
                    user_id =record.id
                    access_token=create_access_token(identity=user_id)
                    refresh_token=create_refresh_token(identity=user_id)
                    return{
                    'access_token':access_token,
                    'refresh_token':refresh_token
                 },200
                    
                else:
                    raise Exception('La contraseña es incorrecta')
            
            raise Exception('No se encontro el Usuario')
            
        except Exception as e :
            return{
                "message":"Ocurrio un Error",
                'error':str(e)
            },500
    
    def refreshToken(self,identity):
        try:
            access_token =create_access_token(identity=identity)
            return {
                'access_token':access_token
            },200
            
        except Exception as e:
            return{
                "message":"Ocurrio un Error",
                'error':str(e)
            },500

    def resetPassword(self,data):
        try :
            email = data['email']
            record = self.model.where(email=email).first()
            if record :
                new_password= token_hex(5)
                record.password=new_password
                record.hashPassword()
                self.mailing.emailResetPassword(record.email,record.name,new_password)

                db.session.add(record)
                db.session.commit()
                return {
                    'message' : f'Se envio un correo con tu nueva contraseña' ,
                },200
            return {
                'message' : 'no existe el usuario' ,
            },404


        except Exception as e:
            db.session.rollback()
            return {
                "message" : "Ocurrio un Error" ,
                'error' : str(e)
            } , 500
