from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from accounting.views import ProductRepo,PersonAccountRepo,AddPersonAccountContext,PersonAccountSerializer
from .serializers import CartItemSerializer,ShopPackageSerializer,ProductSerializer,SupplierSerializer,ShopSerializer
from .repo import CartItemRepo,ShopPackageRepo,SupplierRepo,ShopRepo,CustomerRepo,ShipperRepo
from .forms import *
from .apps import APP_NAME
from .serializers import ShipperSerializer,ProductWithPriceSerializer,CustomerGroupSerializer
from .repo import ShipperRepo,CustomerGroupRepo
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from accounting.views import CategoryRepo
import json
from .enums import *
from django.views import View
from core.views import CoreContext,leolog
from authentication.views import PersonRepo,PersonSerializer,AddPersonContext
from utility.views import RegionRepo
from .serializers import CustomerSerializer
from utility.views import MessageView
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='market/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
        
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    context[WIDE_LAYOUT]=False 
    me_supplier=SupplierRepo(request=request).me
    me_customer=CustomerRepo(request=request).me
    context['market_navbar']=False
    if me_supplier is not None:
        context['market_navbar']=True
        context['me_supplier']=me_supplier
    if me_customer is not None:
        context['market_navbar']=True
        context['me_customer']=me_customer
        context.update(CartItemContext(request=request,customer=me_customer))
    tuman_view=False
    from utility.repo import ParameterRepo
    from phoenix.server_settings import CURRENCY,CURRENCY_TUMAN
    p_repo=ParameterRepo(request=request,app_name=APP_NAME)
    param=p_repo.parameter(name="واحد پولی برای نمایش ( "+CURRENCY+" , "+CURRENCY_TUMAN+" )",default=CURRENCY)
    if param.value==CURRENCY_TUMAN:
        context['SHOW_TUMAN']=True
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def CartItemContext(request,customer,*args, **kwargs):
    context={}
    cart_items=CartItemRepo(request=request).list(customer_id=customer.id)
    cart_items_s=json.dumps(CartItemSerializer(cart_items,many=True).data)
    context['cart_items']=cart_items
    context['cart_items_s']=cart_items_s
    context['cart_items_navbar_s']=cart_items_s
    return context

def AddMarketPersonContext(request):
    context=AddPersonAccountContext(request=request)
    regions=RegionRepo(request=request).list()
    context['regions']=regions
    customer_groups=CustomerGroupRepo(request=request).list()
    context['customer_groups']=customer_groups
    person_accounts=PersonAccountRepo(request=request).list()
    person_accounts_s=json.dumps(PersonAccountSerializer(person_accounts,many=True).data)
    context['person_accounts']=person_accounts
    context['person_accounts_s']=person_accounts_s
 



    return context

def AddSupplierContext(request,*args, **kwargs):
    if not request.user.has_perm(APP_NAME+".add_supplier"):
        return context
    context=AddMarketPersonContext(request=request)
    context['add_supplier_form']=AddSupplierForm()
    return context

def AddCustomerContext(request,*args, **kwargs): 
    if not request.user.has_perm(APP_NAME+".add_customer"):
        return {}
    context=AddMarketPersonContext(request=request) 
    context['add_customer_form']=AddCustomerForm()
    return context

def AddShipperContext(request,*args, **kwargs): 
    if not request.user.has_perm(APP_NAME+".add_shipper"):
        return {}
    context=AddMarketPersonContext(request=request) 
    context['add_shipper_form']=AddShipperForm()
    return context
       
def AddShopPackageContext(request,*args, **kwargs):
    context={}
    return context
    
def AddShopContext(request,*args, **kwargs):
 
    context={}
    context['add_shop_form']=AddShopForm()
    context['unit_names_for_add_shop_app']=(i[0] for i in UnitNameEnum.choices)
    context['unit_names_for_add_shop_app']=(i[0] for i in UnitNameEnum.choices) 
    context['regions_for_add_shop_app']=RegionRepo(request=request).list()
    context['groups_for_add_shop_app']=CustomerGroupRepo(request=request).list()
    return context


class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here.

 
class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products =ProductRepo(request=request).list(*args, **kwargs)
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
 
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"products.html",context) 
    

class CategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        category_repo=CategoryRepo(request=request)
        category=category_repo.category(*args, **kwargs)
        context['category']=category
        from .serializers import CategorySerializer
        category_s=json.dumps(CategorySerializer(category,many=False).data)
        context['category_s']=category_s 


        if category is None:
            categories=category_repo.roots()
            context['category_id']=0
            products=[]
        else:
            categories=category_repo.list(parent_id=category.id)
            products=category.products.all()
            context['category_id']=category.id
            # leolog(all_childs_products=category.all_childs_products())

        context['categories']=categories
        categories_s=json.dumps(CategorySerializer(categories,many=True).data)
        context['categories_s']=categories_s


        for product in products:
            primary_shop=ShopRepo(request=request).primary_shop(product)
            if primary_shop is None:
                product.available=False
            else:
                pass
                product.available=True
                product.unit_name=primary_shop.unit_name
                product.unit_price=primary_shop.unit_price*(100-primary_shop.discount_percentage)/100
            # print(product.available)
            # print(product.default_unit_name)
            # print(product.default_unit_price)
        context['products']=products
        products_s=json.dumps(ProductWithPriceSerializer(products,many=True).data)
        context['products_s']=products_s
 
        return render(request,TEMPLATE_ROOT+"category.html",context)

    
class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product =ProductRepo(request=request).product(*args, **kwargs)
        context['product']=product
        from accounting.views import ProductContext
        context.update(ProductContext(request=request,product=product))
        context[WIDE_LAYOUT]=True
        primary_shop=ShopRepo(request=request).primary_shop(product=product)
        context['primary_shop']=primary_shop

        
        shops=ShopRepo(request=request).list(product_id=product.id)
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops']=shops
        context['shops_s']=shops_s


        me_supplier=SupplierRepo(request=request).me
        if me_supplier is not None:
            context.update(AddShopContext(request=request))

            
        me_customer=CustomerRepo(request=request).me
        if me_customer is not None:
            context['add_cart_line_form']=AddCartLineForm()
            # context.update(AddShopContext(request=request))
            pass

        return render(request,TEMPLATE_ROOT+"product.html",context) 
    
    
class SuppliersView(View):
    def get(self,request,*args,**kwargs):
        context=getContext(request=request)
        suppliers=SupplierRepo(request=request).list(*args,**kwargs)
        suppliers_s=json.dumps(SupplierSerializer(suppliers,many=True).data)
        context['suppliers']=suppliers
        context['suppliers_s']=suppliers_s
        
        if request.user.has_perm(APP_NAME+".add_supplier"):
            context.update(AddSupplierContext(request=request))
        return render(request,TEMPLATE_ROOT+"suppliers.html",context) 


class ShopPackagesView(View):
    def get(self,request,*args,**kwargs):
        context=getContext(request=request)
        shop_packages=ShopPackageRepo(request=request).list(*args,**kwargs)
        shop_packages_s=json.dumps(ShopPackageSerializer(shop_packages,many=True).data)
        context['shop_packages']=shop_packages
        context['shop_packages_s']=shop_packages_s
        
        if request.user.has_perm(APP_NAME+".add_shoppackage"):
            context.update(AddShopPackageContext(request=request))
        return render(request,TEMPLATE_ROOT+"shop-packages.html",context) 


class ShopPackageView(View):
    def get(self,request,*args,**kwargs):
        context=getContext(request=request)
        shop_package=ShopPackageRepo(request=request).shop_package(*args,**kwargs)
        shop_package_s=json.dumps(ShopPackageSerializer(shop_package).data)
        context['shop_package']=shop_package
        context['shop_package_s']=shop_package_s


        shops=shop_package.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops']=shops
        context['shops_s']=shops_s

        if 'me_supplier' in kwargs and context['me_supplier'] is not None:
            context.update(AddShopContext(request=request))
        return render(request,TEMPLATE_ROOT+"shop-package.html",context) 

        
class SupplierView(View):
    def get(self,request,*args,**kwargs):
        context=getContext(request=request)
        supplier=SupplierRepo(request=request).supplier(*args,**kwargs)
        supplier_s=json.dumps(SupplierSerializer(supplier,many=False).data)
        context['supplier']=supplier
        context['supplier_s']=supplier_s
        context['person_account']=supplier.person_account
        context['person']=supplier.person_account.person
        context['account']=supplier.person_account



        # menus =supplier.menu_set.all()
        # context['menus']=menus
        # menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        # context['menus_s']=menus_s

        
        shops=ShopRepo(request=request).list(supplier_id=supplier.id)
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops']=shops
        context['shops_s']=shops_s



        
        shop_packages=ShopPackageRepo(request=request).list(supplier_id=supplier.id)
        shop_packages_s=json.dumps(ShopPackageSerializer(shop_packages,many=True).data)
        context['shop_packages']=shop_packages
        context['shop_packages_s']=shop_packages_s


        return render(request,TEMPLATE_ROOT+"supplier.html",context) 

    
class ShippersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        shippers =ShipperRepo(request=request).list(*args, **kwargs)
        context['shippers']=shippers
        
        shippers_s=json.dumps(ShipperSerializer(shippers,many=True).data)
        context['shippers_s']=shippers_s
        if request.user.has_perm(APP_NAME+'.add_shipper'):
            context.update(AddShipperContext(request=request))
 
        return render(request,TEMPLATE_ROOT+"shippers.html",context) 
    
   
class ShipperView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        shipper =ShipperRepo(request=request).shipper(*args, **kwargs)
        context['shipper']=shipper
        
        shipper_s=json.dumps(ShipperSerializer(shipper,many=False).data)
        context['shipper_s']=shipper_s
 
 
        return render(request,TEMPLATE_ROOT+"shipper.html",context) 
    
    
class CustomerView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        customer =CustomerRepo(request=request).customer(*args, **kwargs)
        context['customer']=customer
        if customer is None:
            msg={}
            msg['title']='خطا'
            msg['body']='خریداری پیدا نشد.'
            mv=MessageView(**msg)
            return mv.get(request=request)   
        customer_s=json.dumps(CustomerSerializer(customer,many=False).data)
        context['customer_s']=customer_s     
        cart_items=CartItemRepo(request=request).list(customer_id=customer.id)
        cart_items_s=json.dumps(CartItemSerializer(cart_items,many=True).data)
        context['cart_items']=cart_items     
        context['cart_items_s']=cart_items_s     


 
 
        return render(request,TEMPLATE_ROOT+"customer.html",context) 
     

class CustomerGroupView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        customer_group =CustomerGroupRepo(request=request).customer_group(*args, **kwargs)
        context['customer_group']=customer_group
        if customer_group is None:
            msg={}
            msg['title']='خطا'
            msg['body']='گروهی پیدا نشد.'
            mv=MessageView(**msg)
            return mv.get(request=request)   
        customer_group_s=json.dumps(CustomerGroupSerializer(customer_group,many=False).data)
        context['customer_group_s']=customer_group_s     
         
        customers=customer_group.customer_set.all()
        
        context['customers']=customers
        
        customers_s=json.dumps(CustomerSerializer(customers,many=True).data)
        context['customers_s']=customers_s
        
        return render(request,TEMPLATE_ROOT+"customer-group.html",context) 
  
    
class CustomersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        customers =CustomerRepo(request=request).list(*args, **kwargs)
        context['customers']=customers
        
        customers_s=json.dumps(CustomerSerializer(customers,many=True).data)
        context['customers_s']=customers_s
        if request.user.has_perm(APP_NAME+'.add_customer'):
            context.update(AddCustomerContext(request=request))
 
        return render(request,TEMPLATE_ROOT+"customers.html",context) 
    
   
    
class CartView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        customer =CustomerRepo(request=request).customer(*args, **kwargs)
        context['customer']=customer
        if customer is None:
            msg={}
            msg['title']='خطا'
            msg['body']='خریداری پیدا نشد.'
            mv=MessageView(**msg)
            return mv.get(request=request)   
        customer_s=json.dumps(CustomerSerializer(customer,many=False).data)
        context['customer_s']=customer_s
 

        context['checkout_cart_form']=CheckoutCartForm()
        cart_items=[]
        if request.user.has_perm(APP_NAME+".view_cartitem"):
            cart_items=CartItemRepo(request=request).list(customer_id=customer.id)
        else:
            me_customer=CustomerRepo(request=request).me
            if me_customer is not None and customer.id==me_customer.id:
                cart_items=CartItemRepo(request=request).list(customer_id=customer.id)

        cart_items_s=json.dumps(CartItemSerializer(cart_items,many=True).data)
        context['cart_items']=cart_items
        context['cart_items_s']=cart_items_s
        context['cart_items_navbar_s']=cart_items_s
 
        return render(request,TEMPLATE_ROOT+"cart.html",context) 
       