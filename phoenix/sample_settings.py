from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'Sth here'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
 
DB_PREFIX_NAME='db_dikoo24ir_phoenix11_v_1_2_0'
ONLY_HTTPS=False
CURRENCY='ریال'
DEBUG = False
DEBUG = True
DATABASE_NAME='20260521_11_41_10'
SITE_URL="/"
PUBLIC_ROOT="d:\\public_html\\phoenix12\\"
PRIVATE_ROOT="d:\\private_html\\phoenix12\\" 

FULL_SITE_URL='http://127.0.0.1:8000/'
  
DB_FILE_NAME=DB_PREFIX_NAME+'__'+DATABASE_NAME 
# DB_FILE_NAME='db_dikoo24ir_phoenix11_v1___1404_12_10_11_59_52' 
# DB_FILE_NAME='db_dikoo24ir_phoenix11_v1___1405_02_18_03_54_42' 
# DB_FILE_NAME='db_dikoo24ir_phoenix11_v1___1405_02_22_10_51_23' 
DB_FILE_NAME='db_dikoo24ir_phoenix11_v1___1405_02_31_02_57_00' 

DB_FILE_PATH=os.path.join(BASE_DIR,DB_FILE_NAME+'.sqlite3')
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_FILE_PATH ,
    }
}
# Application definition
 
 



TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'

COMING_SOON =False

QRCODE_URL =SITE_URL+"qrcode/"
STATIC_URL =SITE_URL+"static/"

TEMPORARY_ROOT =os.path.join(PRIVATE_ROOT,"temp")
UPLOAD_ROOT =os.path.join(PRIVATE_ROOT,"upload")
QRCODE_ROOT =os.path.join(PUBLIC_ROOT,"qrcode")
STATIC_ROOT =os.path.join(PUBLIC_ROOT,"static")
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]

MEDIA_URL =SITE_URL+"media/"
MEDIA_ROOT =os.path.join(PUBLIC_ROOT,"media")

ADMIN_URL=SITE_URL+"admin/"


PUSHER_IS_ENABLE=False

VUE_VERSION_3=False
VUE_VERSION_2=True



 
 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'authentication',
    'blog',
    'authentication'
    
    'core',
    'utility',
    'projectmanager',

]

