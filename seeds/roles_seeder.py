from flask_seeder import Seeder,Faker,generator
from app.models.roles_model import RoleModel

class RoleSeeder(Seeder):
    def run(self):
        roles=[
            {
                'name':'Administrador'
            },
            {
                'name':'Usuario Normal'
            }
        ]

        for role in roles:
            record = RoleModel.where(name=role['name']).first()
            if not record:
                new_record=RoleModel.create(**role)
                self.db.session.add(new_record)
                self.db.session.commit()

        """faker =Faker(
            cls = RoleModel,
            init = {
                "name" :generator.Name()
            }
        )
        for user in  faker.create(3):
            self.db.session.add(user)"""