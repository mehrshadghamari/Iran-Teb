from kavenegar import *

def send_sms(phone_number,text):
    
    try:
        api = KavenegarAPI('your api key')
        
        params = {
            'receptor' : str(phone_number),
            'message' : str(text)
        }   
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
        return True
