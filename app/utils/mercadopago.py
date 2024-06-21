from os import  getenv
from requests import  post,get


class Mercadopago:
    def __init__(self):
        self.main_token=getenv('MERCADOPAGO_MAIN_ACCESS_TOKEN')
        self.child_token=getenv('MERCADOPAGO_CHILD_ACCESS_TOKEN')
        self.main_headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.main_token}'
        }

        self.child_headers={
            'Content-Type' : 'application/json' ,
            'Authorization' : f'Bearer {self.child_token}'
        }


        self.base_url='https://api.mercadopago.com'
        self.site_id='MPE'
    def createUserTest(self,data):
        url=f'{self.base_url}/users/test'
        response=post(
            url,
            json={
                'description':data['description'],
                'site_id':self.site_id
            },
            headers = self.main_headers
        )

        return response.json()

    def createPreferences(self,payer,products,order_correlative):
        url = f'{ self.base_url }/checkout/preferences'
        body = {
            "payer" : payer ,
            "items" :products,
            "external_reference" : order_correlative
        }
        response=post(url,json=body,headers = self.child_headers)
        return  response.json()


    def getPaymentById(self,id):
        url =f'{self.base_url}/v1/payments/{id}'
        response =get(url,headers = self.child_headers)
        return  response.json()