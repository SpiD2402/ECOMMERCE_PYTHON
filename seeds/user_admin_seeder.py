from flask_seeder import Seeder
from  app.models.users_model import UserModel

class UserSeeder(Seeder):
    def run(self):
        users=[
            {
                'name':'Usuarios',
                'last_name':'Administrador',
                'username':'admin',
                'password':'123456',
                'email':'adminsitrador@gmail.com',
                'rol_id':1
            }
        ]
        for user in users:
            record =UserModel.where(username=user['username']).first()
            if not record:
                print('Se crea Usuario')
                new_record =UserModel().create(**user)
                new_record.hashPassword()
                self.db.session.add(new_record)