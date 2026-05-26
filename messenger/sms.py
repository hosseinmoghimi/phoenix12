import ghasedakpack
from core.constants import SUCCEED,FAILED
from utility.log import leolog
from phoenix.server_settings import SMS_API_KEY,SMS_LINE_NUMBER
def send_sms(*args, **kwargs):
    
    
    API_KEY=SMS_API_KEY
    message="hi hossein"
    receptor="09155323633"
    line_number=SMS_LINE_NUMBER

    if 'API_KEY' in kwargs:
        API_KEY=kwargs['API_KEY']

        
    if 'message' in kwargs:
        message=kwargs['message']

        
    if 'receptor' in kwargs:
        receptor=kwargs['receptor']

    if 'line_number' in kwargs:
        line_number=kwargs['line_number']

    # return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number="300002525")
    # return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number="5000121212")
    # return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number="10008642")
    # return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number="5000270")
    # return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number="210002100")
    # return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number="10008566")
    # return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number=line_number)
    return send_sms_(API_KEY=API_KEY,message=message,receptor=receptor,line_number=SMS_LINE_NUMBER)


def send_sms_(API_KEY,message,receptor,line_number,*args, **kwargs):
 
    #create an instance:
    sms = ghasedakpack.Ghasedak(API_KEY)

    #send a single message to a single number:
    sms.send({'message':message, 'receptor' : receptor, 'linenumber': line_number})
    result=SUCCEED
    message_back=f"""پیامک با موفقیت از شماره {line_number} ارسال شد."""
    status_code=200

    return result,message_back,status_code,line_number

    #send a single message to multiple numbers:
    # sms.bulk1({'message':message, 'receptor' : '09xxxxxxxxx,09xxxxxxxxx,09xxxxxxxxx', 'linenumber': '3000xxxxx'})

    #send multiple massages to multiple numbers:
    # sms.bulk2({'message':message, 'receptor' : '09xxxxxxxxx,09xxxxxxxxx,09xxxxxxxxx', 'linenumber': '3000xxxxx'})

    #get the status of massages:
    # print(sms.status({'id': 'messageId', 'type': '1'}))
    data = {
        'path': "sms/status?agent=python",
        'data':{
        'id': 'messageId',
        'type':'1',
        }
    } 
    status_code=sms.request_api(data).status_code
    result=SUCCEED
    if status_code==200:
        message_back=f"""پیامک با موفقیت از شماره {line_number} ارسال شد."""
    else:
        message_back=f"""پیامک با خطای {status_code} در هنگام ارسال از طریق شماره {line_number} مواجه شد."""
        result=FAILED
        # return result,message_back,status_code,line_number


    return result,message_back,status_code,line_number