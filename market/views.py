from django.shortcuts import render,redirect
from utility.constants import INDEX_FOR_ALL_CHOICES
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
LAYOUT_PARENT='market/layout.html'
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

def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False


    products=ProductRepo(request=request).list(search_for=search_for)
    if len(products)>0:
        context['products']=products
        context['products_s']=json.dumps(ProductSerializer(products,many=True).data)
        WAS_FOUND=True


    categories=CategoryRepo(request=request).list(search_for=search_for)
    if len(categories)>0:
        context['categories']=categories
        from .serializers import CategorySerializer
        context['categories_s']=json.dumps(CategorySerializer(categories,many=True).data)
        WAS_FOUND=True


    if WAS_FOUND:
        context['WAS_FOUND']=WAS_FOUND
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
        return (CategoryView().get(request=request,pk=0))

 
class LinksView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"links.html",context)


class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps 
         
        return render(request,TEMPLATE_ROOT+"search.html",context)

    def post(self,request,*args, **kwargs):
        from utility.constants import SUCCEED,FAILED
        
        result=FAILED
        search_for=''
        message=''
        log=1
        context=getContext(request=request) 
        context['WAS_FOUND']=False

        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            log=2
            search_for=search_form.cleaned_data['search_for'] 
            result=SUCCEED
            WAS_FOUND=False
            SEARCH_IN_ALL_APPS=True
  
            
            
            products=ProductRepo(request=request).list(search_for=search_for)
            if len(products)>0:
                context['products']=products
                context['products_s']=json.dumps(ProductSerializer(products,many=True).data)
                WAS_FOUND=True


            categories=CategoryRepo(request=request).list(search_for=search_for)
            if len(categories)>0:
                context['categories']=categories
                from .serializers import CategorySerializer
                context['categories_s']=json.dumps(CategorySerializer(categories,many=True).data)
                WAS_FOUND=True


            if WAS_FOUND:
                context['WAS_FOUND']=WAS_FOUND
                    
                    
             
        context['message']=message
        context['search_for']=search_for
        context['log']=log
        context['result']=result
        if WAS_FOUND:
               context['WAS_FOUND']=WAS_FOUND
        return render(request, TEMPLATE_ROOT+"search.html",context)

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

        


        me_supplier=SupplierRepo(request=request).me
        me_customer=CustomerRepo(request=request).me
        shops=ShopRepo(request=request).list(product_id=product.id)

        if me_supplier is not None:
            context.update(AddShopContext(request=request))


        if me_customer is not None:
            context['add_cart_line_form']=AddCartLineForm()
 

        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops']=shops
        context['shops_s']=shops_s

        return render(request,TEMPLATE_ROOT+"product.html",context) 


class ShopsView(View):
   def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        shops =ShopRepo(request=request).list(*args, **kwargs)
        context['shops']=shops
         

        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops']=shops
        context['shops_s']=shops_s

        if request.user.has_perm(APP_NAME+".add_shop"):
            context['add_shops_form']=AddShopsForm()
            context['suppliers']=SupplierRepo(request=request).list()
            context['groups']=CustomerGroupRepo(request=request).list()
            context['regions']=RegionRepo(request=request).list()

        return render(request,TEMPLATE_ROOT+"shops.html",context) 
     

class ExportShopsToExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        ExportShopsToExcelForm_=ExportShopsToExcelForm(request.POST)
        if ExportShopsToExcelForm_.is_valid():
            cd=ExportShopsToExcelForm_.cleaned_data
            choices={}
            if not cd['group_id']==INDEX_FOR_ALL_CHOICES:
                choices['group_id']=cd['group_id']

            if not cd['region_id']==INDEX_FOR_ALL_CHOICES:
                choices['region_id']=cd['region_id'] 

            if not cd['supplier_id']==INDEX_FOR_ALL_CHOICES:
                choices['supplier_id']=cd['supplier_id']
                
            shops=ShopRepo(request=request).list(**choices)
            return export_to_excel(request=request,shops=shops,EXPORT_SHOPS=True)
    

def export_to_excel(request,*args, **kwargs):
    now=PersianCalendar().date
    date=PersianCalendar().from_gregorian(now)
    EXPORT_SHOPS=False
    if 'EXPORT_SHOPS' in kwargs:
        EXPORT_SHOPS=kwargs['EXPORT_SHOPS']

        
    shops=[]
    if 'shops' in kwargs:
        shops=kwargs['shops']



    if EXPORT_SHOPS:
        lines=[]
        for i,shop in enumerate(shops,start=1):
            line={
                'row':i,
                'id':shop.id,
                'supplier_id':shop.supplier.id,
                'supplier':shop.supplier.person_account.title,
                'product_id':shop.product.id,
                'product_barcode':shop.product.barcode,
                'product':shop.product.title,
                'group_id':shop.group.id,
                'group':shop.group.name,
                'region_id':shop.region.id,
                'region':shop.region.full_name,
                'quantity':shop.quantity,
                'unit_name':shop.unit_name,
                'discount_percentage':shop.discount_percentage,
                'unit_price':shop.unit_price,
                'start_date':PersianCalendar().from_gregorian(shop.start_date),
                'end_date':PersianCalendar().from_gregorian(shop.end_date),
            }
            lines.append(line)
        headers=['ردیف',
                'شناسه',
                'کد فروشنده',
                'فروشنده',
                'کد کالا',
                'بارکد کالا',
                'کالا',
                'کد گروه',
                'گروه',
                'کد منطقه',
                'منطقه',
                'تعداد',
                'واحد',
                'درصد تخفیف',
                'قیمت جزء',
                'تاریخ شروع',
                'تاریخ پایان',
        ]
        
        from .constants import EXCEL_SHOPS_DATA_START_ROW
        start_row=EXCEL_SHOPS_DATA_START_ROW
        if start_row>2:
            start_row-=1
        
        
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'market.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')

        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='shops',
            title='shops',
        )
        
    file_name=f"""Phoenix market {date.replace('/','').replace(':','')}.xlsx"""
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
    response["Content-disposition"]=f"attachment; filename={file_name}"
    report_work_book.work_book.save(response)
    report_work_book.work_book.close()
    return response
    
     
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
       