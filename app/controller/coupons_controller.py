from app.models.coupons_model import CouponModel
from app.schemas.coupons_schema import CouponResponseSchema
from app import db
from pytz import  timezone
from datetime import datetime
class CouponsController:
    def __init__(self):
        self.model = CouponModel
        self.schema = CouponResponseSchema


        self.timezone = timezone('America/Lima')
        self.datetimenow=datetime.now(tz = self.timezone)
        self.datenow= self.datetimenow.strftime('%Y:%m:%d')
        self.hournow = self.datetimenow.strftime('%H:%M:%S')
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
    def validate(self,code):
          try:
              record = self.model.where(code=code).first()
              if record:
                  return  self._validateDateTimeCoupon(record),200
              return {
                  'message' : 'No se encontro el cupon mencionado' ,
              },404
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
                  'message' : 'Coupon creado'
              },200
          except Exception as e:
              db.session.rollback()
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def getById(self,id):
          try:
              record= self.model.where(id=id,status=True).first()
              response = self.schema(many=False)
              if record:
                  return{
                      'data':response.dump(record)
                  },200
              return {
                  'message' : 'Coupon not found'
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
                    'message' : 'Coupon modificado'
                },200
            return {
                'message' : 'Coupon no encontrado'
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
                      'message' : 'Coupon deshabilitado'
                  }

          except Exception as e:
              db.session.rollback()
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def _validateDateTimeCouponToOrder(self,code):

        record = self.model.where(code = code).first()

        if record:
            started_date=datetime.strftime(record.started_at,'%Y-%m-%d')
            started_hour=datetime.strftime(record.started_at,'%H:%M:%S')

            ended_date=datetime.strftime(record.ended_at,'%Y-%m-%d')
            ended_hour=datetime.strftime(record.ended_at,'%H:%M:%S')

            #Validar las fechas
            if self.datenow < started_date or self.datenow > ended_date:
                return None

            #Validar que estemos en la hora de inicio
            if self.datenow == started_date and self.hournow < started_hour:
                return None

            #Validar que estemos en la hora antes de vencer
            if self.datenow == ended_date and  self.hournow > ended_hour:
                return None

            return  record.percentage
        return  None


    def _validateDateTimeCoupon(self,record):
        started_date=datetime.strftime(record.started_at,'%Y-%m-%d')
        started_hour=datetime.strftime(record.started_at,'%H:%M:%S')

        ended_date=datetime.strftime(record.ended_at,'%Y-%m-%d')
        ended_hour=datetime.strftime(record.ended_at,'%H:%M:%S')

        #Validar las fechas
        if self.datenow < started_date or self.datenow > ended_date:
            raise Exception('El cupon aun no empieza  o ya vencio')

        #Validar que estemos en la hora de inicio
        if self.datenow == started_date and self.hournow < started_hour:
            raise Exception('El cupon aun no puede ser usado')

        #Validar que estemos en la hora antes de vencer
        if self.datenow == ended_date and  self.hournow > ended_hour:
            raise Exception('El cupon a vencido')

        response =self.schema(many=False)
        return  response.dump(record)

