from app.models.base import BaseModel
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from bcrypt import hashpw,gensalt,checkpw
from sqlalchemy.orm import relationship

class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True , autoincrement=True)
    name = Column(String(80))
    last_name = Column(String(120))
    username = Column(String(80) , unique=True)
    password = Column(String(120) , nullable=False)
    email = Column(String(140) , unique=True)
    rol_id = Column(Integer , ForeignKey('roles.id'))
    role = relationship('RoleModel',uselist=False,back_populates='users')

    status = Column(Boolean , default=True)
    
    def hashPassword(self):
        pwd_encode=  self.password.encode('utf-8')
        pwd_hash= hashpw(pwd_encode,gensalt(rounds=10))
        self.password= pwd_hash.decode('utf-8')
        
    
    def checkPassword(self,password):
        return checkpw(
            
            password.encode('utf-8'),
            self.password.encode('utf-8')
            
        )