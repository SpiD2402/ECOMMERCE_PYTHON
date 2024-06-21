from sqlalchemy import Column , Integer , String , Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
class CategoryModel(BaseModel):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True,autoincrement = True)
    name= Column(String(120))
    status=Column(Boolean,default = True)

    products= relationship('ProductModel',uselist = True,back_populates = 'category')