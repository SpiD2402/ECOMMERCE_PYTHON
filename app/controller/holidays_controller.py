from app.models.holidays_model import HolidayModel
from locale import setlocale, LC_ALL
from app import  db
from app.schemas.holidays_schema import HolidayResponseSchema,DeliveryDateResponseSchema
from pytz import  timezone
from datetime import datetime,timedelta
class HolidaysController:
    def __init__(self):
        self.model = HolidayModel
        self.schema = HolidayResponseSchema


        self.__max_count=5
        self.__start_hour ="09:00:00"
        self.__end_hour ="21:00:00"
        self.__not_work=[6]
        self.timezone = timezone('America/Lima')
        self.datetimenow=datetime.now(tz = self.timezone)
        self.hournow= self.datetimenow.strftime('%H:%M:%S')
        setlocale(LC_ALL,'es_PE')


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
                  'message' : 'Holiday creado'
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
                  'message' : 'Holiday not found'
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
                    'message' : 'Holiday modificado'
                },200
            return {
                'message' : 'Holiday no encontrado'
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

          except Exception as e:
              db.session.rollback()
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500

    def deliveryDate(self):
          try:
              records=self.model.where(status =True).order_by('date').all()
              holidays= []
              if records:
                  #for record in records:
                  #    holidays.append(
                  #        datetime.strftime(record.date,'%d-%#m')
                  #    )
                  holidays.extend(datetime.strftime(record.date,'%d-%#m') for record in records)

              date_now =self.datetimenow.date()
              if self.hournow > self.__end_hour or self.hournow < self.__start_hour:
                  date_now+= timedelta(days=1)

              count = 0
              delivery_dates = []
              while count< self.__max_count:
                  date_now += timedelta(days = 1)
                  if date_now.weekday() not  in self.__not_work  and f'{date_now.day}-{date_now.month}' not in holidays:
                      delivery_dates.append(
                          {
                              'date' : date_now,
                              'format':datetime.strftime(
                                  date_now,'%A, %d de %B '
                              )
                           }
                      )
                      count+=1
              response = DeliveryDateResponseSchema(many = True)
              print(delivery_dates)
              return {
                  'data':response.dump(delivery_dates)
              },200
          except Exception as e:
              return {
                  'message' : 'ocurrio un error' ,
                  'error' : str(e)
              } , 500