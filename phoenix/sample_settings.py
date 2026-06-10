SECRET_KEY = 'Sth here'
DB_PREFIX_NAME='db_phoenix12_v_0_0_3'


from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
ALLOWED_HOSTS = ['dikoo24.ir']
 
ONLY_HTTPS=False
CURRENCY='ریال'
CURRENCY_TUMAN='تومان'
DEBUG = False
DEBUG = True
DATABASE_NAME='20260521_17_20_10'
SITE_URL="/"
PUBLIC_ROOT="/home/dikooir/public_html/phoenix12/"
PRIVATE_ROOT="/home/dikooir/private_html/phoenix12/"

FULL_SITE_URL='http://dikoo24.ir/'
  
DB_FILE_NAME=DB_PREFIX_NAME+'__'+DATABASE_NAME   

DB_FILE_PATH=os.path.join(BASE_DIR,DB_FILE_NAME+'.sqlite3')
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_FILE_PATH ,
    }
} 



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
    'utility',
    'authentication',
    'core',
    'log',
    'attachments',
    'blog',
    'messenger',
    'accounting',
    'organization',
    'projectmanager',
    'warehouse',
    'market',
    'cafe',
    'bms',
    'django_social_share',


    'allauth',   # <--
    'allauth.account',   # <--
    'allauth.socialaccount',   # <--
    'allauth.socialaccount.providers.google',   # <--



]

