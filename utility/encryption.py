from cryptography.fernet import Fernet
from phoenix.constants import FAILED, SUCCEED
from utility.log import leolog

import base64
def fixed32lengthkey(key):
    
    a=len(key)
    if a==32:
        return key
    if a>32:
        return key[:32]
    return key+((32-a)*"*")

def str2base64(message,*args, **kwargs):
    if 'encoding' in kwargs:
        encoding=kwargs['encoding']
    else:
        encoding='ascii'

    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_string = base64_bytes.decode(encoding)
    return base64_string,base64_bytes


class Encrptor:

    def __init__(self,*args, **kwargs):
        if 'key' in kwargs and kwargs['key'] is not None and len(kwargs['key'])>0:
            self.key=kwargs['key']
            self.key=fixed32lengthkey(self.key)
            # self.key=self.key.encode("utf-8")
            # self.key=self.key.encode('ascii')
            # base64_bytes = base64.b64encode(self.key)
            # base64_string = base64_bytes.decode("utf-8")
            base64_string,base64_bytes=str2base64(message=self.key,encoding="utf-8")
            self.key=base64_bytes
           

        else:
            self.key = Fernet.generate_key()

    def encrypt(self,plain,*args, **kwargs):
        self.fernet = Fernet(self.key)
        encMessage = self.fernet.encrypt(plain.encode())
        return encMessage


    def decrypt(self,cypher,*args, **kwargs):
        encoding = 'utf-8'
        cypher=bytearray(cypher,encoding)
        cypher=bytes(cypher)
        # self.key=bytearray(self.key,encoding)
        # self.key=bytes(self.key)
        self.fernet = Fernet(self.key)
        decMessage=""
        try:
            decMessage = self.fernet.decrypt(cypher).decode()
            result=SUCCEED
        except:
            result=FAILED
        return result,decMessage

