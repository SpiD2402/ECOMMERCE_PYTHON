from app import db

from app.models.orders_model import OrderModel
from app.utils.mercadopago import  Mercadopago


class MercadopagoController:
    def __init__(self):
        self.model = OrderModel
        self.mercadopago =Mercadopago()

    def updatePaymentStatus(self,payment_id):
        payment =self.mercadopago.getPaymentById(payment_id)
        status = payment['status']
        status_detail=payment['status_detail']
        external_reference = int(payment['external_reference'])
        record = self.model.where(id=external_reference).first()
        if record:
            record.payment_status = status
            record.payment_detail = status_detail
            record.status = status

            db.session.add(record)
            db.session.commit()