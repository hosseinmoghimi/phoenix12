from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import TableRepo
from .serializers import TableSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,MessageView
from phoenix.server_apps import phoenix_apps
from market.serializers import ShopSerializer

from utility.calendar import PersianCalendar
import json

from .serializers import MenuSerializer,TableSerializer
from .repo import MenuRepo,TableRepo

from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='cafe/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def AddTableContext(request,*args, **kwargs):
    context={}
    from market.views import SupplierRepo,SupplierSerializer
    suppliers=SupplierRepo(request=request).list()
    suppliers_s=json.dumps(SupplierSerializer(suppliers,many=True).data)
    context['suppliers_s']=suppliers_s
    context['suppliers']=suppliers
    return context

def AddMenuContext(request,*args, **kwargs):
    context={}
    from market.views import SupplierRepo,SupplierSerializer
    suppliers=SupplierRepo(request=request).list()
    suppliers_s=json.dumps(SupplierSerializer(suppliers,many=True).data)
    context['suppliers_s']=suppliers_s
    context['suppliers']=suppliers
    return context
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)


class TableView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        table =TableRepo(request=request).table(*args, **kwargs)
        context['table']=table
        
        menus=table.supplier.menu_set.all()
        menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        context['menus']=menus
        context['menus_s']=menus_s
 
  
        context['NOT_NAVBAR']=True
        context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"table.html",context) 
    
     
class TablesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        tables =TableRepo(request=request).list(*args, **kwargs)
        context['tables']=tables
        
        tables_s=json.dumps(TableSerializer(tables,many=True).data)
        context['tables_s']=tables_s
        if request.user.has_perm(APP_NAME+'.add_table'):
            context['add_table_form']=AddTableForm()
            context.update(AddTableContext(request=request))
        return render(request,TEMPLATE_ROOT+"tables.html",context) 
    

class MenusView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menus =MenuRepo(request=request).list(*args, **kwargs)
        context['menus']=menus
        menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        context['menus_s']=menus_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_menu"):
            context['add_menu_form']=AddMenuForm()
            from market.views import SupplierRepo
            suppliers=SupplierRepo(request=request).list()
            context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+"menus.html",context) 
    

class MenuView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        from market.views import CustomerRepo,CartItemRepo,ShopSerializer
        menu =MenuRepo(request=request).menu(*args, **kwargs) 
        context['menu']=menu
        menu_s=json.dumps(MenuSerializer(menu,many=False).data)
        context['menu_s']=menu_s

        shops=menu.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops_s']=shops_s

  
 

        context[WIDE_LAYOUT]=True
        # context['NOT_NAVBAR']=True
        # context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"menu.html",context) 
 

class OrderView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menus =MenuRepo(request=request).list(*args, **kwargs)
        context['menus']=menus
        menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        context['menus_for_order_app']=menus_s
        context['menus_s']=menus_s

        tables =TableRepo(request=request).list(*args, **kwargs)
        context['tables']=tables
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_menu"):
            context['add_menu_form']=AddMenuForm()
             
        return render(request,TEMPLATE_ROOT+"order.html",context) 
    
