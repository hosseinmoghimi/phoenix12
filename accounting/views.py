from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from utility.log import leolog
from .constants import EXCEL_PRODUCTS_DATA_START_ROW,EXCEL_SERVICES_DATA_START_ROW,EXCEL_CATEGORIES_DATA_START_ROW,EXCEL_ACCOUNTS_DATA_START_ROW
from django.http import Http404,HttpResponse
from django.views import View
from .enums import *
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.excel import ReportWorkBook,get_style
from utility.calendar import PersianCalendar
from core.views import CoreContext,PageContext
from .repo import FinancialDocumentRepo,CategoryRepo,BrandRepo,AssetRepo,ChequeRepo
from .repo import PersonCategoryRepo,PersonRepo,ServiceRepo,FAILED,SUCCEED,InvoiceLineItemRepo,FinancialDocumentLineRepo,AccountRepo
from .repo import ProductRepo,InvoiceRepo,FinancialEventRepo,PersonAccountRepo
from .repo import  BankAccountRepo,InvoiceLineRepo
from .serializers import BankAccountSerializer
from .serializers import ServiceSerializer,FinancialDocumentSerializer,CategorySerializer,BrandSerializer,ChequeSerializer
from .serializers import InvoiceLineItemSerializer,AccountBriefSerializer,InvoiceLineItemUnitSerializer,InvoiceLineWithInvoiceSerializer,InvoiceLineSerializer,AccountSerializer,ProductSerializer,InvoiceSerializer,FinancialEventSerializer,FinancialDocumentLineSerializer
from .serializers import FinancialYearSerializer,ProductSpecificationSerializer,PersonAccountSerializer
from .serializers import PersonCategorySerializer,AssetSerializer,BankSerializer
from .repo import FinancialYearRepo,BankRepo
from authentication.views import PersonContext,PersonSerializer
from utility.currency import to_price_colored
import json 
from log.repo import LogRepo
from core.views import MessageView
from .models import UnitNameEnum
from django.shortcuts import reverse,redirect



LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='accounting/'
WIDE_LAYOUT=True
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    # context['WIDE_LAYOUT']=WIDE_LAYOUT
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
def AddBrandContext(request,*args, **kwargs):
    context={}
    context['add_brand_form']=AddBrandForm()
    return context

def AddBankAccountContext(request,*args, **kwargs):
    context=AddAccountContext(request=request,*args, **kwargs)
    context['add_bank_account_form']=AddBankAccountForm()
    banks_for_add_bank_account=BankRepo(request=request).list(*args, **kwargs)
    context['banks_for_add_bank_account']=banks_for_add_bank_account
    if 'person' in kwargs:
        person=kwargs['person']
        # context['person']=person
        person_s=json.dumps(PersonSerializer(person).data)
        # context['person_s']=person_s
        context['person_s_for_add_bank_account']=json.dumps(PersonSerializer(person).data)
    context['account_natures_for_add_bank_account']=(i[0] for i in AccountNatureEnum.choices)
    return context

def AddAccountContext(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_account"):
        context['account_natures_for_add_account']=(i[0] for i in AccountNatureEnum.choices)
        context['account_natures_for_add_person_account']=(f[0] for f in AccountNatureEnum.choices)
        context['add_account_form']=AddAccountForm()
    return context

def AddAssetContext(request,*args, **kwargs):
    context={}
    context['add_asset_form']=AddAssetForm()
    return context

def AddInvoiceLineItemContext(request,*args, **kwargs):
    context={}
    unit_names=(i[0] for i in UnitNameEnum.choices)
    context['unit_names_for_add_invoice_line_item']=unit_names
    return context

def AssetContext(request,asset,*args, **kwargs):
    context={}
    context.update(PageContext(request=request,page=asset))
    context['asset']=asset
    asset_s=json.dumps(AssetSerializer(asset).data)
    context['asset_s']=asset_s
    return context

def AddProductContext(request,*args, **kwargs):
    context=AddInvoiceLineItemContext(request=request)
    brands=BrandRepo(request=request).list()
    context['brands_for_add_product_app']=brands
    categories=CategoryRepo(request=request).list()
    context['categories_for_add_product_app']=categories
    categories_s=json.dumps(CategorySerializer(categories,many=True).data)
    context['categories_for_add_product_app_s']=categories_s
    context['import_products_from_excel_form']=ImportProductsFromExcelForm()
    context['import_categories_from_excel_form']=ImportCategoriesFromExcelForm()
    context['add_product_form']=AddProductForm()
    return context

def AddServiceContext(request):
    context=AddInvoiceLineItemContext(request=request)
    context['import_services_from_excel_form']=ImportServicesFromExcelForm()
    context['add_service_form']=AddServiceForm()
    return context

def AddInvoiceLineContext(request,*args, **kwargs):
    context={}
    unit_names=(i[0] for i in UnitNameEnum.choices)
    context["unit_names_for_add_invoice_line"]=unit_names
    context["unit_names_for_edit_invoice_line"]=unit_names
    unit_names2=[]
    for ii in UnitNameEnum.choices:
        unit_names2.append(str(ii[0]))
    context["unit_names_for_edit_invoice_line_s"]=json.dumps(unit_names2)
    invoice_line_statuses=(i[0] for i in InvoiceLineStatusEnum.choices)
    context["invoice_line_statuses"]=invoice_line_statuses
    context["add_invoice_line_form"]=AddInvoiceLineForm
    invoice_line_items=InvoiceLineItemRepo(request=request).list()
    invoice_line_items_s=json.dumps(InvoiceLineItemSerializer(invoice_line_items,many=True).data)
    context["invoice_line_items_s"]=invoice_line_items_s

    
    # products=ProductRepo(request=request).list()
    # products_s=json.dumps(ProductSerializer(products,many=True).data)
    # context["products_s"]=products_s

    
    # services=ServiceRepo(request=request).list()
    # services_s=json.dumps(ServiceSerializer(services,many=True).data)
    # context["services_s"]=services_s
    return context
 
def AccountsContext(request):
    context={}
    accounts=AccountRepo(request=request).list().order_by('title')
    accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
    context['accounts']=accounts
    context['accounts_s']=accounts_s
    return context

def AccountContext(request,account,*args, **kwargs):

    context=PageContext(request=request,page=account)
    if account is None:
        return None 
    
    logs=LogRepo(request=request).list(url=account.get_absolute_url())
    context['logs']=logs
    context.update(AddFinancialDocumentLineContext(request=request,account=account))       
    person_account=PersonAccountRepo(request=request).person_account(pk=account.pk)
    if person_account is not None:
        context.update(PersonContext(request=request,person=person_account.person))
        account=person_account

    bank_account=BankAccountRepo(request=request).bank_account(pk=account.pk)
    if bank_account is not None:
        context['bank_account']=bank_account
        account=bank_account
    context['account']=account 
    account_s=json.dumps(AccountSerializer(account).data)
    context['account_s']=account_s

    
    financial_document_lines=account.financialdocumentline_set.all()

    context['financial_document_lines']=financial_document_lines
    financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
    context['financial_document_lines_s']=financial_document_lines_s
    context['print_financial_document_lines_form']=PrintFinancialDocumentLinesForm()


 
    all_sub_accounts_lines=account.all_sub_accounts_lines().order_by('date_time') 
    all_sub_accounts_lines_s=json.dumps(FinancialDocumentLineSerializer(all_sub_accounts_lines,many=True).data)
    context['all_sub_accounts_lines_s']=all_sub_accounts_lines_s
    context['financial_document_lines']=all_sub_accounts_lines
    context['financial_document_lines_s']=all_sub_accounts_lines_s
    context['print_financial_document_lines_form']=PrintFinancialDocumentLinesForm()


    
    financial_events=FinancialEventRepo(request=request).list(account_id=account.id)
    financial_events_s=json.dumps(FinancialEventSerializer(financial_events,many=True).data)
    context['financial_events']=financial_events
    context['financial_events_s']=financial_events_s 



    accounts =AccountRepo(request=request).list(parent_id=account.id)
    context['accounts']=accounts
    if len(accounts)>0:
        context['expand_accounts']=True
    accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
    context['accounts_s']=accounts_s
 
    if request.user.has_perm(APP_NAME+".add_account"):
        context.update(AddAccountContext(request=request))
    return context

def InvoiceLineItemContext(request,invoice_line_item,*args, **kwargs):
    context=PageContext(request=request,page=invoice_line_item)

    context['invoice_line_item']=invoice_line_item
    invoice_lines=InvoiceLineRepo(request=request).list(invoice_line_item_id=invoice_line_item)
    # invoice_lines=invoice_line_item.invoiceline_set.order_by('row')
    context['invoice_lines']=invoice_lines
    invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
    context['invoice_lines_s']=invoice_lines_s

    from .repo import InvoiceLineItemUnitRepo
    invoice_line_item_units=InvoiceLineItemUnitRepo(request=request).list(invoice_line_item_id=invoice_line_item.id)
    invoice_line_item_units_s=json.dumps(InvoiceLineItemUnitSerializer(invoice_line_item_units,many=True).data)
    context['invoice_line_item_units']=invoice_line_item_units
    context['invoice_line_item_units_s']=invoice_line_item_units_s
    if request.user.has_perm(APP_NAME+".add_invoicelineitemunit"):
        context.update(AddInvoiceLineItemUnitsContext(request=request,invoice_line_item=invoice_line_item))
    return context

def AddInvoiceLineItemUnitsContext(request,invoice_line_item,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_invoicelineitemunit"):
        context["add_invoice_line_item_unit_form"]=AddInvoiceLineItemUnitForm()
        context['unit_names']=(i[0] for i in UnitNameEnum.choices)
        context['base_price']=0
    return context

def AddFinancialDocumentLineContext(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+'.add_financialdocumentline'):
        context['financial_document_line_statuses']=(i[0] for i in FinancialDocumentStatusEnum.choices)
        context['add_financial_document_line_form']=AddFinancialDocumentLineForm()
    # if 'financial_event' in kwargs:
    #     context['financial_event']='financial_event'
    # if 'financial_document' in kwargs:
    #     context['financial_document']='financial_document'
    # if 'event' in kwargs:
    #     context['event']='event'
    return context

def FinancialEventContext(request,financial_event):
    context={}
    context['financial_event']=financial_event 
    context.update(PageContext(request=request,page=financial_event))
    
    context['financial_event']=financial_event
    financial_event_s=json.dumps(FinancialEventSerializer(financial_event).data)
    context['financial_event_s']=financial_event_s

    if request.user.has_perm(APP_NAME+'add_financialdocumentline'):
        context.update(AddFinancialDocumentLineContext(request=request,financial_event=financial_event))
    
    financial_document_lines=FinancialDocumentLineRepo(request=request).list(financial_event_id=financial_event.id).order_by('-bedehkar')
    financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
 
    context["financial_document_lines_s"]=financial_document_lines_s
    if request.user.has_perm(APP_NAME+'.change_financialevent'):
        if financial_event.status==FinancialEventStatusEnum.DELIVERED or financial_event.status==FinancialEventStatusEnum.APPROVED or financial_event.status==FinancialEventStatusEnum.FINISHED:
            context['make_financial_event_draft_form']=MakeFinancialEventDraftForm()
        else:
            payment_methods=(i[0] for i in PaymentMethodEnum.choices)
            financial_event_statuses=(i[0] for i in FinancialEventStatusEnum.choices)
            context['financial_event_statuses']=financial_event_statuses
            context['payment_methods_for_edit_financial_event_form']=payment_methods
            context['edit_financial_event_form']=EditFinancialEventForm()

    return context

def InvoiceContext(request,invoice,*args, **kwargs):
    context=FinancialEventContext(request=request,financial_event=invoice)
    if invoice.status==FinancialEventStatusEnum.APPROVED:
        pass
    elif invoice.status==FinancialEventStatusEnum.DELIVERED:
        pass
    elif invoice.status==FinancialEventStatusEnum.FINISHED: 
        pass 
    else:
        context.update(AddInvoiceLineContext(request=request))
    context['invoice'] = invoice
    invoice_s=json.dumps(InvoiceSerializer(invoice).data)
    context['invoice_s'] =invoice_s

    SHOW_LINES=True
    if SHOW_LINES:
        invoice_lines=invoice.invoiceline_set.order_by('row')
        context['invoice_lines']=invoice_lines
        invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context['invoice_lines_s']=invoice_lines_s
    
    if request.user.has_perm(APP_NAME+'.change_invoice'):

        if invoice.status==FinancialEventStatusEnum.DELIVERED or invoice.status==FinancialEventStatusEnum.APPROVED or invoice.status==FinancialEventStatusEnum.FINISHED:
            context['make_financial_event_draft_form']=MakeFinancialEventDraftForm()
        else: 
            payment_methods=(i[0] for i in PaymentMethodEnum.choices)
            invoice_statuses=(i[0] for i in FinancialEventStatusEnum.choices)
            context['invoice_statuses']=invoice_statuses
            context['payment_methods_for_edit_invoice_form']=payment_methods
            context['edit_invoice_form']=EditFinancialEventForm()
    
    try:
        if 'warehouse' in kwargs and kwargs['warehouse']:
            from warehouse.views import WareHouseSheetRepo,WareHouseSheetSerializer,AddInvoiceWareHouseSheetsForm
            warehouse_sheets=WareHouseSheetRepo(request=request).list(invoice_id=invoice.id).order_by('date_added')
            context["warehouses"]=warehouse_sheets
            warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
            context["warehouse_sheets_s"]=warehouse_sheets_s  
            ADD_WAREHOUSE_SHEETS=True
            if ADD_WAREHOUSE_SHEETS:
                from organization.views import OrganizationalUnitRepo
                from warehouse.views import WareHouseRepo,WareHouseSheetDirectionEnum,SignatureStatusEnum,WareHouseSheetTypeEnum
                organizational_units=OrganizationalUnitRepo(request=request).list()
                warehouses=WareHouseRepo(request=request).list()
                directions=(i[0] for i in WareHouseSheetDirectionEnum.choices)
                context['organizational_units_for_add_invoice_warehouse_sheets_app']=organizational_units
                context['warehouses_for_add_invoice_warehouse_sheets_app']=warehouses
                context['directions_for_add_invoice_warehouse_sheets_app']=directions
                context['add_invoice_warehouse_sheets_form']=AddInvoiceWareHouseSheetsForm()

                statuses=(i[0] for i in SignatureStatusEnum.choices)
                types=(i[0] for i in WareHouseSheetTypeEnum.choices)
                context['statuses_for_add_warehouse_sheet_app']=statuses
                context['types_for_add_warehouse_sheet_app']=types
    except:
        pass
    return context
     
def ProductContext(request,product,*args, **kwargs):
    context=InvoiceLineItemContext(request=request,invoice_line_item=product)
    
    context.update(AddProductToCategoryContext(request=request,product=product))


    product_specifications=product.productspecification_set.all()
    product_specifications_s=json.dumps(ProductSpecificationSerializer(product_specifications,many=True).data)
    context['product_specifications']=product_specifications
    context['product_specifications_s']=product_specifications_s
    
    if request.user.has_perm(APP_NAME+".add_productspecification"):
        context["add_product_specification_form"]=AddProductSpecificationForm()
        specification_names=['رنگ','وزن','اندازه','جرم','نوع','حجم',]
        context['specification_names']=specification_names
    context['product']=product

 
    
    if request.user.has_perm(APP_NAME+".change_product"):
        context['add_product_to_category_form']=AddProductToCategoryForm()
        categories=CategoryRepo(request=request).list()
        context['categories']=categories
        product_categories=product.category_set.all()
        all_product_categories=categories
        product_categories_s=json.dumps(CategorySerializer(product_categories,many=True).data)
        all_product_categories_s=json.dumps(CategorySerializer(all_product_categories,many=True).data)
        context['product_categories_s']=product_categories_s
        context['all_product_categories_s']=all_product_categories_s

    return context
   
def ServiceContext(request,service,*args, **kwargs):
    context={}
    context.update(InvoiceLineItemContext(request=request,invoice_line_item=service))
    context["service"]=service
    return context

def AddFinancialEventContext(request):
    context={}
    context['add_financial_event_form']=AddFinancialEventForm()
    person_accounts=PersonAccountRepo(request=request).list()
    statuses=(i[0] for i in FinancialEventStatusEnum.choices)
    context['statuses_for_add_financial_event']=statuses
    context['person_accounts']=person_accounts
    return context

def ChequeContext(request,cheque):
    context=FinancialEventContext(request=request,financial_event=cheque)
    context['cheque']=cheque
    return context

def AddChequeContext(request):
    context=AddFinancialEventContext(request=request)
    context['add_cheque_form']=AddChequeForm()
    return context

def AddInvoiceContext(request):
    context=AddFinancialEventContext(request=request)
    invoice_statuses=(i[0] for i in FinancialEventStatusEnum.choices)
    context['invoice_statuses']=invoice_statuses
    context['add_invoice_form']=AddInvoiceForm()
    return context

def AddFinancialDocumentContext(request):
    context={}
    
    if request.user.has_perm(APP_NAME+'.add_financialdocument'):
        current_financial_year=FinancialYearRepo(request=request).current_financial_year()
        if current_financial_year is None:
            return {}

        context['add_financial_document_form']=AddFinancialDocumentForm()
        context['current_financial_year_id']=current_financial_year.id
        context['financial_year_statuses']=(i[0] for i in FinancialYearStatusEnum.choices)
    return context

def AddProductToCategoryContext(request,product,*args, **kwargs):
    context={}

    category_repo=CategoryRepo(request=request)
    all_categories=category_repo.list()
    all_categories_s=json.dumps(CategorySerializer(all_categories,many=True).data)
    context['all_categories_s']=all_categories_s

    
    product_categories=product.category_set.all()
    product_categories_s=json.dumps(CategorySerializer(product_categories,many=True).data)
    context['product_categories_s']=product_categories_s
    return context

def EditFinancialDocumentContext(request,financial_document,*args, **kwargs):
    context={}
    context['edit_financial_document_form']=EditFinancialDocumentForm()
    context['statuses_for_edit_financial_document_form']=(i[0] for i in FinancialDocumentStatusEnum.choices)
    return context

def AddPersonCategoryContext(request,*args, **kwargs):
    context={}
    context['add_person_category_form']=AddPersonCategoryForm()
    return context

def AddPersonAccountContext(request,*args, **kwargs):
    context=AddAccountContext(request=request)
    person_categories=PersonCategoryRepo(request=request).list()
    context['person_categories']=person_categories
    context['add_person_account_form']=AddPersonAccountForm()
    return context

def PersonAccountContext(request,person_account,*args, **kwargs):
    context=AccountContext(request=request,account=person_account,*args, **kwargs)
    context['person_account']=person_account
    person_account_s=json.dumps(PersonAccountSerializer(person_account).data)
    context['person_account_s']=person_account_s
    return context

def BankAccountContext(request,bank_account,*args, **kwargs):
    context=AccountContext(request=request,account=bank_account,*args, **kwargs)
    context['bank_account']=bank_account
    bank_account_s=json.dumps(BankAccountSerializer(bank_account).data)
    context['bank_account_s']=bank_account_s
    return context

def AddBankContext(request,*args, **kwargs):
    context={}
    return context

def BankContext(request,bank,*args, **kwargs):
    context={}
    context['bank']=bank
    bank_s=json.dumps(BankSerializer(bank).data)
    context['bank_s']=bank_s
    return context


def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False

    accounts=AccountRepo(request=request).list(search_for=search_for)
    if len(accounts)>0:
        context['accounts']=accounts
        context['accounts_s']=json.dumps(AccountSerializer(accounts,many=True).data)
        WAS_FOUND=True


    bank_accounts=BankAccountRepo(request=request).list(search_for=search_for)
    if len(bank_accounts)>0:
        context['bank_accounts']=bank_accounts
        context['bank_accounts_s']=json.dumps(BankAccountSerializer(bank_accounts,many=True).data)
        WAS_FOUND=True


        

    invoices=InvoiceRepo(request=request).list(search_for=search_for)
    if len(invoices)>0:
        context['invoices']=invoices
        context['invoices_s']=json.dumps(InvoiceSerializer(invoices,many=True).data)
        WAS_FOUND=True

        

    financial_events=FinancialEventRepo(request=request).list(search_for=search_for)
    if len(financial_events)>0:
        context['financial_events']=financial_events
        context['financial_events_s']=json.dumps(FinancialEventSerializer(financial_events,many=True).data)
        WAS_FOUND=True

        

    financial_documents=FinancialDocumentRepo(request=request).list(search_for=search_for)
    if len(financial_documents)>0:
        context['financial_documents']=financial_documents
        context['financial_documents_s']=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
        WAS_FOUND=True



    financial_document_lines=FinancialDocumentLineRepo(request=request).list(search_for=search_for)
    if len(financial_document_lines)>0:
        context['financial_document_lines']=financial_document_lines
        context['financial_document_lines_s']=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
        WAS_FOUND=True


        

    persons=PersonRepo(request=request).list(search_for=search_for)
    if len(persons)>0:
        context['persons']=persons
        context['persons_s']=json.dumps(PersonSerializer(persons,many=True).data)
        WAS_FOUND=True


    products=ProductRepo(request=request).list(search_for=search_for)
    if len(products)>0:
        context['products']=products
        context['products_s']=json.dumps(ProductSerializer(products,many=True).data)
        WAS_FOUND=True


    brands=BrandRepo(request=request).list(search_for=search_for)
    if len(brands)>0:
        context['brands']=brands
        context['brands_s']=json.dumps(BrandSerializer(brands,many=True).data)
        WAS_FOUND=True

        

    services=ServiceRepo(request=request).list(search_for=search_for)
    if len(services)>0:
        context['services']=services
        context['services_s']=json.dumps(ServiceSerializer(services,many=True).data)
        WAS_FOUND=True

        

    categories=CategoryRepo(request=request).list(search_for=search_for)
    if len(categories)>0:
        context['categories']=categories
        context['categories_s']=json.dumps(CategorySerializer(categories,many=True).data)
        WAS_FOUND=True

    if WAS_FOUND:
               context['WAS_FOUND']=WAS_FOUND
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
 

class HelpView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"help.html",context)
 

class SettingsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        # accounts =AccountRepo(request=request).roots(*args, **kwargs)
        # context['accounts']=accounts
        if request.user.has_perm(APP_NAME+'.view_product'):
            context['import_from_excel_form']=ImportFromExcelForm()
        return render(request,TEMPLATE_ROOT+"settings.html",context) 


class InvoiceToExcelView(View):
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        if invoice is None:
            mv=MessageView(request=request)
            mv.title="فاکتور پیدا نشد."
            mv.body="فاکتور پیدا نشد."
            return mv.response()
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        for i,invoice_line in enumerate(invoice.invoiceline_set.all(),start=1):
            line={
                'row':i,
                'title':invoice_line.invoice_line_item.title,
                'quantity':str(to_normal_number(invoice_line.quantity)) +' '+ invoice_line.unit_name,      
                'discount':invoice_line.discount,      
                'unit_price':invoice_line.unit_price,      
                'line_total':invoice_line.line_total,      
            }
            lines.append(line)
        headers=['ردیف',
                 'عنوان',
                 'تعداد', 
                 'تخفیف',
                 'فی',
                 'مبلغ'
        ]
        
        report_work_book=ReportWorkBook(origin_file_name=f'Invoice.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='Invoice',
        )
            
        file_name=f"""Phoenix Invoice {invoice.pk} {date.replace('/','').replace(':','')}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response


class FinancialYearsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_years=FinancialYearRepo(request=request).list(*args, **kwargs)
        context['expand_financial_years']=True
        context['financial_years']=financial_years
        financial_years_s=json.dumps(FinancialYearSerializer(financial_years,many=True).data)
        context['financial_years_s']=financial_years_s
        if request.user.has_perm(APP_NAME+".add_financialyear"):
            context['add_financial_year_form']=AddFinancialYearForm()
            context['add_financial_year_form_statuses']=(i[0] for i in FinancialYearStatusEnum.choices)
            context['default_status']=FinancialYearStatusEnum.DRAFT
        return render(request,TEMPLATE_ROOT+"financial-years.html",context)


class FinancialYearView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_year=FinancialYearRepo(request=request).financial_year(*args, **kwargs)
        context['WIDE_LAYOUT']=True
        if financial_year is None:
            from core.views import MessageView
            mv=MessageView()
            context={}
            back_url = request.META.get('HTTP_REFERER')
            context['back_url'] = back_url
            context["title"]="سال مالی وجود ندارد."
            context["body"]="چنین سال مالی وجود ندارد."
            return mv.get(request=request,**context)

        context['financial_year']=financial_year
        
        financial_documents=FinancialDocumentRepo(request=request).list(financial_year_id=financial_year.id)
        context['financial_documents']=financial_documents
        financial_documents_s=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
        context['financial_documents_s']=financial_documents_s

        return render(request,TEMPLATE_ROOT+"financial-year.html",context)


class TreeChartView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context[WIDE_LAYOUT]=True
        
        context=getContext(request=request)
        if 'pk' in kwargs and not int(kwargs["pk"])==0:
            account=AccountRepo(request=request).account(*args, **kwargs)

            accounts=account.all_childs()
            context['account']=account
        else:
            accounts=AccountRepo(request=request).list(*args, **kwargs)

        context['accounts']=accounts
        pages=[]
         
        AG=100
        BA=100000
        MA=100000000
        MA2=10000000000
        for account in accounts:
            pages.append({
                'title': f"""{account.code}<br>{account.name}""",
                'parent_id': account.parent_id,
                'parent': 0,
                'get_absolute_url': account.get_absolute_url(),
                'id': account.id,
                'pre_title': "",
                'color': account.color,
                'sub_title':to_price_colored(account.balance),
                })

        context['pages_s'] = json.dumps(pages)
        return render(request,TEMPLATE_ROOT+"tree-chart.html",context) 


class TreeListView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        accounts =AccountRepo(request=request).roots(*args, **kwargs)
        context['accounts']=accounts
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"tree-list.html",context) 


class FinancialDocumentLinesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_document_lines=FinancialDocumentLineRepo(request=request).list(*args, **kwargs)

        context['financial_document_lines']=financial_document_lines
        financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
        context['financial_document_lines_s']=financial_document_lines_s
        context['print_financial_document_lines_form']=PrintFinancialDocumentLinesForm()
        context['expand_financial_document_lines']=True
        context['WIDE_LAYOUT']=True

        return render(request,TEMPLATE_ROOT+"financial-document-lines.html",context)


class FinancialDocumentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_document=FinancialDocumentRepo(request=request).financial_document(*args, **kwargs)
        if financial_document is None:
            mv=MessageView()
            title='سند پیدا نشد.'
            body='سند پیدا نشد.'
            mv.message={'title':title,'body':body}
            return mv.get(request=request) 
        context['financial_document']=financial_document
        financial_document_s=json.dumps(FinancialDocumentSerializer(financial_document).data)
        context['financial_document_s']=financial_document_s

        logs=LogRepo(request=request).list(url=financial_document.get_absolute_url())
        context['logs']=logs

        financial_document_lines=financial_document.financialdocumentline_set.order_by('-date_time')

        context['financial_document_lines']=financial_document_lines
        financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
        context['financial_document_lines_s']=financial_document_lines_s
        context['print_financial_document_lines_form']=PrintFinancialDocumentLinesForm()

        if request.user.has_perm(APP_NAME+'.add_financialdocumentline'):
            context.update(AddFinancialDocumentLineContext(request=request,financial_document=financial_document))
             

        if request.user.has_perm(APP_NAME+'.edit_financialdocumentline'):
            context.update(EditFinancialDocumentContext(request=request,financial_document=financial_document))
             

        return render(request,TEMPLATE_ROOT+"financial-document.html",context)


class FinancialDocumentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_documents=FinancialDocumentRepo(request=request).list()
        context['financial_documents']=financial_documents
        financial_documents_s=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
        context['financial_documents_s']=financial_documents_s
        current_financial_year=FinancialYearRepo(request=request).current_financial_year()
        if current_financial_year is None:
            from attachments.models import Link,reverse
            title='ابتدا سال مالی جاری را ایجاد کنید.'
            
            color1='success'
            title1='سال های مالی'
            url1=reverse('accounting:financial_years')
            # link1={'color':color1,'url':url1,'title':title1}
            link1=Link(title=title1,url=url1,color='success')

            color2='danger'
            title2='اسناد مالی'
            url2=reverse('accounting:financial_documents')
            # link2={'color':color2,'url':url2,'title':title2}
            link2=Link(title=title2,url=url2,color='danger')
            links=[link1,link2]
            mv=MessageView(title=title,links=links)
            return mv.get(request=request)
        context.update(AddFinancialDocumentContext(request=request))
        return render(request,TEMPLATE_ROOT+"financial-documents.html",context)


class FinancialDocumentLineView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        financial_document_line=FinancialDocumentLineRepo(request=request).financial_document_line(*args, **kwargs)
        context['financial_document_line']=financial_document_line
        financial_document_line_s=json.dumps(FinancialDocumentLineSerializer(financial_document_line).data)
        context['financial_document_line_s']=financial_document_line_s
        
        logs=LogRepo(request=request).list(url=financial_document_line.get_absolute_url())
        context['logs']=logs

        context['account_s']=json.dumps(AccountSerializer(financial_document_line.account).data)
        context['financial_event_s']=json.dumps(FinancialEventSerializer(financial_document_line.financial_event).data)
        context['financial_document_s']=json.dumps(FinancialDocumentSerializer(financial_document_line.financial_document).data)
        context['persian_date_time']=financial_document_line.persian_date_time_[0:10]
        if request.user.has_perm(APP_NAME+'.change_financialdocumentline'):
            context['edit_financial_document_line_form']=EditFinancialDocumentLineForm()
            context['financial_document_line_statuses']=(i[0] for i in FinancialDocumentStatusEnum.choices)
        return render(request,TEMPLATE_ROOT+"financial-document-line.html",context)


class AddInvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if request.user.has_perm(APP_NAME+'.add_invoice'):
            
            context.update(AddInvoiceContext(request=request))
        else:
            title='شما مجوز افزودن فاکتور ندارید.'
            body='شما مجوز افزودن فاکتور ندارید.'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        return render(request,TEMPLATE_ROOT+"add-invoice.html",context)
    def post(self,request,*args, **kwargs):
        from .apis import AddInvoiceApi
        return AddInvoiceApi().post(request=request,*args, **kwargs)


class FinancialDocumentLinesPrintView(View):
    def post(self,request,*args, **kwargs):
        print_financial_document_lines_form=PrintFinancialDocumentLinesForm(request.POST)
        if print_financial_document_lines_form.is_valid():
            kwargs=print_financial_document_lines_form.cleaned_data
            context=getContext(request=request) 

            financial_document_lines_ids=kwargs['financial_document_lines_ids']
            financial_document_lines_ids=json.loads(financial_document_lines_ids)
            financial_document_lines=FinancialDocumentLineRepo(request=request).list(id__in=financial_document_lines_ids)
            context['financial_document_lines']=financial_document_lines
            from .serializers import FinancialDocumentLineForPrintSerializer
            financial_document_lines_s=json.dumps(FinancialDocumentLineForPrintSerializer(financial_document_lines,many=True).data)
            context['financial_document_lines_s']=financial_document_lines_s
            context['print_financial_document_lines_form']=PrintFinancialDocumentLinesForm()

            if 'account_id' in kwargs:
                account=AccountRepo(request=request).account(account_id=kwargs['account_id'])
                if account is not None:
                    context['account']=account
                    context['account_s']=json.dumps(AccountSerializer(account).data)
            if 'financial_event_id' in kwargs:
                financial_event=FinancialEventRepo(request=request).financial_event(financial_event_id=kwargs['financial_event_id'])
                if financial_event is not None:
                    context['financial_event']=financial_event
                    context['financial_event_s']=json.dumps(FinancialEventSerializer(financial_event).data)
            if 'financial_document_id' in kwargs:
                financial_document=FinancialDocumentRepo(request=request).financial_document(financial_document_id=kwargs['financial_document_id'])
                if financial_document is not None:
                    context['financial_document']=financial_document
                    context['financial_document_s']=json.dumps(FinancialDocumentSerializer(financial_document).data)
            if 'person_id' in kwargs:
                person=PersonRepo(request=request).person(person_id=kwargs['person_id'])
                if person is not None:
                    context['person']=person
                    context['person_s']=json.dumps(PersonSerializer(person).data)
            
        else:
            title="داده های نا معتبر"
            body="داده های ورودی معتبر نمی باشند"
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)    
        context['NOT_REPONSIVE']=True
        context['NOT_NAVBAR']=True
        context['NOT_FOOTER']=True
        context['WIDE_LAYOUT']=False
        return render(request,TEMPLATE_ROOT+"financial-document-lines-print.html",context)


class AccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        context['expand_accounts']=True
        accounts=AccountRepo(request=request).list(*args, **kwargs)

        context['accounts']=accounts
        accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
        context['accounts_s']=accounts_s
        context.update(AddAccountContext(request=request))
        if request.user.has_perm(APP_NAME+".delete_account"):
            context['merge_account_form']=MergeAccountForm()
        return render(request,TEMPLATE_ROOT+"accounts.html",context)


class PersonView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        person=PersonRepo(request=request).person(*args, **kwargs)



        if person is None:
            title='خطا'
            body='شخص پیدا نشد.'

            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        context.update(PersonContext(request=request,person=person))
                 
        person_accounts=PersonAccountRepo(request=request).list(person_id=person.id)

        context['person_accounts']=person_accounts
        person_accounts_s=json.dumps(PersonAccountSerializer(person_accounts,many=True).data)
        context['person_accounts_s']=person_accounts_s





        bank_accounts=person.bankaccount_set.all()

        context['bank_accounts']=bank_accounts
        bank_accounts_s=json.dumps(BankAccountSerializer(bank_accounts,many=True).data)
        context['bank_accounts_s']=bank_accounts_s


        accounts_ids=[]
        for bank_account in bank_accounts:
            accounts_ids.append(bank_account.id)
        for person_account in person_accounts:
            accounts_ids.append(person_account.id)

        financial_document_lines=FinancialDocumentLineRepo(request=request).list(account_id__in=accounts_ids)
        financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
        context['financial_document_lines_s']=financial_document_lines_s
        context['financial_document_lines']=financial_document_lines
        context['print_financial_document_lines_form']=PrintFinancialDocumentLinesForm()


        if request.user.has_perm(APP_NAME+'.add_personaccount'):
            context.update(AddPersonAccountContext(request=request))
        if request.user.has_perm(APP_NAME+'.add_bankaccount'):
            context.update(AddBankAccountContext(request=request))
            
        return render(request,TEMPLATE_ROOT+"person.html",context)


class AccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        account=AccountRepo(request=request).account(*args, **kwargs)


        if account is None:
            title='خطا'
            body='حساب پیدا نشد.'

            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        context.update(AccountContext(request=request,account=account))
         

        return render(request,TEMPLATE_ROOT+"account.html",context)


class SelectionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)

        account_groups=AccountRepo(request=request).list(level=0,*args, **kwargs)
        context['account_groups']=account_groups
        account_groups_s=json.dumps(AccountBriefSerializer(account_groups,many=True).data)
        context['account_groups_s']=account_groups_s

        

        basic_accounts=AccountRepo(request=request).list(level=1,*args, **kwargs)
        context['basic_accounts']=basic_accounts
        basic_accounts_s=json.dumps(AccountBriefSerializer(basic_accounts,many=True).data)
        context['basic_accounts_s']=basic_accounts_s


        moein_accounts=AccountRepo(request=request).list(level=2,*args, **kwargs)
        context['moein_accounts']=moein_accounts
        moein_accounts_s=json.dumps(AccountBriefSerializer(moein_accounts,many=True).data)
        context['moein_accounts_s']=moein_accounts_s

         
        moein2_accounts=AccountRepo(request=request).list(level=3,*args, **kwargs)
        context['moein2_accounts']=moein2_accounts
        moein2_accounts_s=json.dumps(AccountBriefSerializer(moein2_accounts,many=True).data)
        context['moein2_accounts_s']=moein2_accounts_s


        context['WIDE_LAYOUT']=True
        return render(request,TEMPLATE_ROOT+"selection.html",context)


class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products =ProductRepo(request=request).list(*args, **kwargs)
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s

        if request.user.has_perm(APP_NAME+".add_product"):
            context.update(AddProductContext(request=request)) 
        if request.user.has_perm(APP_NAME+".change_product"):
            context['merge_product_form']=MergeProductForm()
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"products.html",context) 
 

class InvoiceLineItemView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice_line_item=InvoiceLineItemRepo(request=request).invoice_line_item(*args, **kwargs)
        if invoice_line_item is None:
            raise Http404
        

        context.update(InvoiceLineItemContext(request=request,invoice_line_item=invoice_line_item))

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"invoice-line-item.html",context)
       
    
class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        if product is None:
            title='کالای مورد نظر یافت نشد.'
            body='کالای مورد نظر یافت نشد.'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context["WIDE_LAYOUT"]=True

        context.update(ProductContext(request=request,product=product))


        from warehouse.views import WareHouseSheetRepo,WareHouseSheetSerializer,ProductInWareHouseRepo,ProductInWareHouseSerializer

        warehouse_sheets=WareHouseSheetRepo(request=request).list(product_id=product.id)
        context["warehouses"]=warehouse_sheets
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context["warehouse_sheets_s"]=warehouse_sheets_s



        products_in_warehouse=ProductInWareHouseRepo(request=request).list(product_id=product.id)

        context["products_in_warehouse"]=products_in_warehouse
        products_in_warehouse_s=json.dumps(ProductInWareHouseSerializer(products_in_warehouse,many=True).data)
        context["products_in_warehouse_s"]=products_in_warehouse_s


        from projectmanager.views import RemoteClientRepo,RemoteClientSerializer

        remote_clients=RemoteClientRepo(request=request).list(product_id=product.id)
        context["warehouses"]=remote_clients
        remote_clients_s=json.dumps(RemoteClientSerializer(remote_clients,many=True).data)
        context["remote_clients_s"]=remote_clients_s

        return render(request,TEMPLATE_ROOT+"product.html",context)
    

class InvoiceLineView(View):
    def get(self,request,*args, **kwargs):
        from warehouse.views import WareHouseSheetRepo,WareHouseSheetSerializer

        context=getContext(request=request)
        invoice_line=InvoiceLineRepo(request=request).invoice_line(*args, **kwargs)
        if invoice_line is None :
            mv=MessageView(title='خطا',body='سطر فاکتور مورد نظر یافت نشد.')
            return mv.get(request=request)
        
        context['invoice_line']=invoice_line
        context.update(InvoiceLineItemContext(request=request,invoice_line_item=invoice_line.invoice_line_item))

        context['phoenix_apps']=phoenix_apps


        warehouse_sheets=WareHouseSheetRepo(request=request).list(invoice_line_id=invoice_line.id)
        context["warehouses"]=warehouse_sheets
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context["warehouse_sheets_s"]=warehouse_sheets_s

        context['WIDE_LAYOUT']=True
        if request.user.has_perm('warehouse.add_warehousesheet'):
            from warehouse.views import AddWareHouseSheetContext
            context.update(AddWareHouseSheetContext(request=request)) 
        return render(request,TEMPLATE_ROOT+"invoice-line.html",context)
    

class ServiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service=ServiceRepo(request=request).service(*args, **kwargs)
        if service is None:
            raise Http404
        

        context.update(ServiceContext(request=request,service=service))

        return render(request,TEMPLATE_ROOT+"service.html",context)   


class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list(*args, **kwargs)
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services']=services
        context['services_s']=services_s
        if request.user.has_perm(APP_NAME+'.add_service'):
            context.update(AddServiceContext(request=request))
        return render(request,TEMPLATE_ROOT+"services.html",context)


class ChequeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        cheque=ChequeRepo(request=request).cheque(*args, **kwargs)
        if cheque is None:
            raise Http404
        

        context.update(ChequeContext(request=request,cheque=cheque))

        return render(request,TEMPLATE_ROOT+"cheque.html",context)   


class ChequesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        cheques=ChequeRepo(request=request).list(*args, **kwargs)
        cheques_s=json.dumps(ChequeSerializer(cheques,many=True).data)
        context['cheques']=cheques
        context['cheques_s']=cheques_s
        if request.user.has_perm(APP_NAME+'.add_cheque'):
            context.update(AddChequeContext(request=request))
        return render(request,TEMPLATE_ROOT+"cheques.html",context)


class ChangeChequeImageView(View):
     def post(self,request,*args, **kwargs):
        log=1
        change_cheque_image_form=ChangeChequeImageForm(request.POST,request.FILES)
        if change_cheque_image_form.is_valid():
            log=3              
            cheque_id=change_cheque_image_form.cleaned_data['cheque_id']
            image=request.FILES['image']
            result,message,cheque=ChequeRepo(request=request).change_image(cheque_id=cheque_id,
            image=image,
            )
            if result==SUCCEED:
                return redirect(reverse(APP_NAME+":cheque",kwargs={'pk':cheque.id}))
        body='چک پیدا نشد'
        title='چک پیدا نشد'
        mv=MessageView(title=title,body=body,)
        return mv.get(request=request)


class AssetView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        asset=AssetRepo(request=request).asset(*args, **kwargs)
        if asset is None:
            raise Http404
        

        context.update(AssetContext(request=request,asset=asset))

        return render(request,TEMPLATE_ROOT+"asset.html",context)   


class AssetsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        assets=AssetRepo(request=request).list(*args, **kwargs)
        assets_s=json.dumps(AssetSerializer(assets,many=True).data)
        context['assets']=assets
        context['assets_s']=assets_s
        if request.user.has_perm(APP_NAME+'.add_asset'):
            context.update(AddAssetContext(request=request))
        return render(request,TEMPLATE_ROOT+"assets.html",context)


class ReportView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['WIDE_LAYOUT']=True

        financial_document_lines=[]

        context['financial_document_lines']=financial_document_lines
        financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
        context['financial_document_lines_s']=financial_document_lines_s
        return render(request,TEMPLATE_ROOT+"report.html",context)   

    def post(self,request,*args, **kwargs):
        from .apis import GetReportApi
        return GetReportApi().post(request=request)


class ServiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service=ServiceRepo(request=request).service(*args, **kwargs)
        if service is None:
            raise Http404
        

        context.update(ServiceContext(request=request,service=service))

        return render(request,TEMPLATE_ROOT+"service.html",context)   


class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list(*args, **kwargs)
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services']=services
        context['services_s']=services_s
        if request.user.has_perm(APP_NAME+'.add_service'):
            context.update(AddServiceContext(request=request))
        return render(request,TEMPLATE_ROOT+"services.html",context)


class ExportProductsToExcelView(View):
    def get(self,request,*args, **kwargs):
        
        EXPORT_CATEGORIES=True
        EXPORT_PRODUCTS=True
        EXPORT_SERVICES=False
        EXPORT_ACCOUNTS=False
        return ExportToExcelView().get(request=request,
                                       EXPORT_CATEGORIES=EXPORT_CATEGORIES,
                                       EXPORT_PRODUCTS=EXPORT_PRODUCTS,
                                       EXPORT_SERVICES=EXPORT_SERVICES,
                                       EXPORT_ACCOUNTS=EXPORT_ACCOUNTS)
         



class ExportCategoriesToExcelView(View):
    def get(self,request,*args, **kwargs):
        
        EXPORT_CATEGORIES=True
        EXPORT_PRODUCTS=False
        EXPORT_SERVICES=False
        EXPORT_ACCOUNTS=False
        return ExportToExcelView().get(request=request,
                                       EXPORT_CATEGORIES=EXPORT_CATEGORIES,
                                       EXPORT_PRODUCTS=EXPORT_PRODUCTS,
                                       EXPORT_SERVICES=EXPORT_SERVICES,
                                       EXPORT_ACCOUNTS=EXPORT_ACCOUNTS)
         


class ExportToExcelView(View):
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        date=PersianCalendar().from_gregorian(now)

        
        report_work_book=ReportWorkBook(origin_file_name=f'accounting.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        EXPORT_CATEGORIES=True
        EXPORT_PRODUCTS=True
        EXPORT_SERVICES=True
        EXPORT_ACCOUNTS=True

        if 'EXPORT_CATEGORIES' in kwargs:
            EXPORT_CATEGORIES=kwargs['EXPORT_CATEGORIES']

        if 'EXPORT_PRODUCTS' in kwargs:
            EXPORT_PRODUCTS=kwargs['EXPORT_PRODUCTS']

        if 'EXPORT_SERVICES' in kwargs:
            EXPORT_SERVICES=kwargs['EXPORT_SERVICES']

        if 'EXPORT_ACCOUNTS' in kwargs:
            EXPORT_ACCOUNTS=kwargs['EXPORT_ACCOUNTS']

        if EXPORT_CATEGORIES:
            
            
            categories=CategoryRepo(request=request).list()
            
                
            lines=[]
            for i,category in enumerate(categories,start=1):
                line={
                    'row':i,
                    'id':category.id,
                    'title':category.title,
                    'parent_id':category.parent_id if category.parent is not None else "",      
                    'thumbnail_origin':str(category.thumbnail_origin),       
                }
                lines.append(line)
            headers=['ردیف',
                    'شناسه',
                    'عنوان',
                    'کد والد', 
                    'تصویر',
            ]
          
            
            start_row=EXCEL_CATEGORIES_DATA_START_ROW
            if start_row>2:
                start_row-=1
            report_work_book.add_sheet(
                data=lines,
                start_row=start_row,
                table_has_header=False,
                table_headers=headers,
                style=style,
                sheet_name='categories',
                title='categories',
            )

           
        if EXPORT_PRODUCTS:
            
            
            products=ProductRepo(request=request).list()
            
                
            lines=[]
            for i,product in enumerate(products,start=1):
                category_id=0
                category=product.category
                if category is not None:
                    category_id=category.id
                line={
                    'row':i,
                    'id':product.id,
                    'title':product.title,
                    'barcode':product.barcode,      
                    'unit_name':product.unit_name,      
                    'unit_price':product.unit_price,       
                    'thumbnail_origin':str(product.thumbnail_origin),       
                    'category_id':category_id,
                }
                lines.append(line)
            headers=['ردیف',
                    'شناسه',
                    'عنوان',
                    'بارکد', 
                    'واحد',
                    'فی',
                    'تصویر',
                    'شناسه دسته بندی',
            ]
          
            
            start_row=EXCEL_PRODUCTS_DATA_START_ROW
            if start_row>2:
                start_row-=1
            report_work_book.add_sheet(
                data=lines,
                start_row=start_row,
                table_has_header=False,
                table_headers=headers,
                style=style,
                sheet_name='products',
                title='products',
            )

            
        if EXPORT_SERVICES:
            
            
            services=ServiceRepo(request=request).list()
            
                
            lines=[]
            for i,service in enumerate(services,start=1):
                line={
                    'row':i,
                    'id':service.id,
                    'title':service.title,
                    'unit_name':service.unit_name,      
                    'unit_price':service.unit_price,       
                    'thumbnail_origin':str(service.thumbnail_origin),       
                }
                lines.append(line)
            headers=['ردیف',
                    'شناسه',
                    'عنوان',
                    'واحد',
                    'فی',
                    'تصویر',
            ]
         
            start_row=EXCEL_SERVICES_DATA_START_ROW
            if start_row>2:
                start_row-=1
            report_work_book.add_sheet(
                data=lines,
                start_row=start_row,
                table_has_header=False,
                table_headers=headers,
                style=style,
                sheet_name='services',
                title='services',
            )
        
     
        if EXPORT_ACCOUNTS:
            
            
            accounts=AccountRepo(request=request).list()
            
                
            lines=[]
            for i,account in enumerate(accounts,start=1):
                line={
                    'row':i,
                    'parent_code':account.parent_account.code if account.parent_account is not None else '',      
                    'id':account.id,
                    'code':account.code,      
                    'title':account.title,
                    'color':account.color,
                    'thumbnail_origin':str(account.thumbnail_origin),       
                }
                lines.append(line)
            headers=['ردیف',
                    'کد والد',
                    'شناسه',
                    'کد',
                    'عنوان',
                    'رنگ',
                    'تصویر',
            ]
         
            start_row=EXCEL_SERVICES_DATA_START_ROW
            if start_row>2:
                start_row-=1
            report_work_book.add_sheet(
                data=lines,
                start_row=start_row,
                table_has_header=False,
                table_headers=headers,
                style=style,
                sheet_name='accounts',
                title='accounts',
            )
        
        file_name=f"""Phoenix accounting {date.replace('/','').replace(':','')}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response


class ExportServicesToExcelView(View):
  
    def get(self,request,*args, **kwargs):
        
        EXPORT_PRODUCTS=False
        EXPORT_SERVICES=True
        EXPORT_ACCOUNTS=False
        return ExportToExcelView().get(request=request,
                                       EXPORT_PRODUCTS=EXPORT_PRODUCTS,
                                       EXPORT_SERVICES=EXPORT_SERVICES,
                                       EXPORT_ACCOUNTS=EXPORT_ACCOUNTS)
          

class FinancialEventView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_event=FinancialEventRepo(request=request).financial_event(*args, **kwargs)
        context.update(FinancialEventContext(request=request,financial_event=financial_event))
        context['financial_event']=financial_event
        from log.repo import LogRepo
        logs=LogRepo(request=request).list(url=financial_event.get_absolute_url())
        context['logs']=logs

        context['WIDE_LAYOUT']=True 
        return render(request,TEMPLATE_ROOT+"financial-event.html",context)


class NewFinancialEventView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        context['WIDE_LAYOUT']=False
        context['expand_add_financial_event']=True
        if request.user.has_perm(APP_NAME+'.add_financialevnt'):
            context.update(AddFinancialEventContext(request=request))
        return render(request,TEMPLATE_ROOT+"new-financial-event.html",context)


class FinancialEventsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_events=FinancialEventRepo(request=request).list()
        financial_events_s=json.dumps(FinancialEventSerializer(financial_events,many=True).data)
        context['financial_events']=financial_events
        context['financial_events_s']=financial_events_s
        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+'.add_financialevnt'):
            context.update(AddFinancialEventContext(request=request))
        return render(request,TEMPLATE_ROOT+"financial-events.html",context)


class MakeFinancialEventDraftView(View):
    def post(self,request,*args, **kwargs):
        make_financial_event_draft_form=MakeFinancialEventDraftForm(request.POST)
        if make_financial_event_draft_form.is_valid():
            cd=make_financial_event_draft_form.cleaned_data
            financial_event=FinancialEventRepo(request=request).financial_event(pk=int(cd['financial_event_id']))
            if financial_event is None:
                title='خطا'
                body='رویداد مالی پیدا نشد.'
                mv=MessageView(title=title,body=body)
                return mv.get(request=request)

            stat=financial_event.status
            financial_event.status=FinancialEventStatusEnum.ROLL_BACKED
            financial_event.save()
            from log.repo import LogRepo
            log_repo=LogRepo(request=request)
            kw={}
            kw['title']='برگشت رویداد مالی'
            kw['url']=financial_event.get_absolute_url()
            kw['app_name']=APP_NAME
            person=PersonRepo(request=request).me
            kw['person_id']=person.id
            kw['description']=f"""رویداد مالی   <a href="{financial_event.get_absolute_url()}">{financial_event.title}</a> """+f'از وضعیت {stat} به وضعیت پیش نویس برگشت کرد.'

            log_repo.add_log(**kw)
            return redirect(financial_event.get_absolute_url())
        else:
            title='خطا'
            body='پارامتر های ورودی صحیح نمی باشد.'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        

class InvoicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoices=InvoiceRepo(request=request).list().order_by('-event_datetime')
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s
        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".add_invoice"):
            context.update(AddInvoiceContext(request=request))
        return render(request,TEMPLATE_ROOT+"invoices.html",context)


class NewInvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        context['WIDE_LAYOUT']=True
        context['expand_new_invoice']=True
        if request.user.has_perm(APP_NAME+".add_invoice"):
            context.update(AddInvoiceContext(request=request))
        return render(request,TEMPLATE_ROOT+"invoice-new.html",context)


class InvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['WIDE_LAYOUT']=True
        context['expand_invoice_lines']=True
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        if invoice is None:
            title='فاکتور پیدا نشد.'
            message='فاکتور پیدا نشد.'
            mv=MessageView(title=title,message=message)
            return mv.get(request=request)
        context['invoice']=invoice
        invoice_s=json.dumps(InvoiceSerializer(invoice,many=False).data)
        context['invoice_s']=invoice_s
        context.update(InvoiceContext(request=request,invoice=invoice,warehouse=True))

        
  

        return render(request,TEMPLATE_ROOT+"invoice.html",context)


class InvoiceEditView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['WIDE_LAYOUT']=True
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        context['invoice']=invoice
        invoice_s=json.dumps(InvoiceSerializer(invoice,many=False).data)
        context['invoice_s']=invoice_s
        context.update(InvoiceContext(request=request,invoice=invoice))
        context.update(AddInvoiceLineContext(request=request))
        context['bedehkar_s']=json.dumps(AccountBriefSerializer(invoice.bedehkar).data)
        context['bestankar_s']=json.dumps(AccountBriefSerializer(invoice.bestankar).data)
        context['invoice_statuses_for_edit_invoice']=(i[0] for i in FinancialEventStatusEnum.choices)
        context['invoice_payment_methods_for_edit_invoice']=(i[0] for i in PaymentMethodEnum.choices)
        return render(request,TEMPLATE_ROOT+"invoice-edit.html",context)

    def post(self,request,*args, **kwargs):
        from .apis import EditInvoiceApi
        return EditInvoiceApi().post(request,*args, **kwargs)


class InvoiceOfficialPrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        if invoice is None:
            title='فاکتور پیدا نشد.'
            message='فاکتور پیدا نشد.'
            mv=MessageView(title=title,message=message)
            return mv.get(request=request)
        
        from attachments.repo import PagePrintRepo,PagePrintTypeEnum
        PagePrintRepo(request=request).add_page_print(page_id=invoice.id,official=True,printed=False)
        context['add_page_print_form']=True
        context['add_page_print_form_type']=PagePrintTypeEnum.OFFICIAL

        context['invoice']=invoice
        context['NOT_REPONSIVE']=True
        context['NOT_NAVBAR']=True
        context['WIDE_LAYOUT']=False
        context['title']=invoice.title
        context['NOT_FOOTER']=True
        invoice_s=json.dumps(InvoiceSerializer(invoice,many=False).data)
        context['invoice_s']=invoice_s
        context.update(InvoiceContext(request=request,invoice=invoice))
        return render(request,TEMPLATE_ROOT+"invoice-official-print.html",context)


class InvoicePrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        if invoice is None:
            title='فاکتور پیدا نشد.'
            message='فاکتور پیدا نشد.'
            mv=MessageView(title=title,message=message)
            return mv.get(request=request)
        from attachments.repo import PagePrintRepo,PagePrintTypeEnum
        PagePrintRepo(request=request).add_page_print(page_id=invoice.id,draft=True,printed=False)
        context['add_page_print_form']=True
        context['add_page_print_form_type']=PagePrintTypeEnum.DRAFT
        context['invoice']=invoice
        context['NOT_REPONSIVE']=True
        context['NOT_NAVBAR']=True
        context['NOT_FOOTER']=True
        context['WIDE_LAYOUT']=False
        context['title']=invoice.title
        invoice_s=json.dumps(InvoiceSerializer(invoice,many=False).data)
        context['invoice_s']=invoice_s
        context.update(InvoiceContext(request=request,invoice=invoice))
        return render(request,TEMPLATE_ROOT+"invoice-print.html",context)


class InvoiceEstelamView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        if invoice is None:
            title='فاکتور پیدا نشد.'
            message='فاکتور پیدا نشد.'
            mv=MessageView(title=title,message=message)
            return mv.get(request=request)
        from attachments.repo import PagePrintRepo,PagePrintTypeEnum
        PagePrintRepo(request=request).add_page_print(page_id=invoice.id,draft=True,printed=False)
        context['add_page_print_form']=True
        context['add_page_print_form_type']=PagePrintTypeEnum.DRAFT
        context['invoice']=invoice
        context['NOT_REPONSIVE']=True
        context['NOT_NAVBAR']=True
        context['WIDE_LAYOUT']=False
        context['title']=invoice.title
        context['NOT_FOOTER']=True
        invoice_s=json.dumps(InvoiceSerializer(invoice,many=False).data)
        context['invoice_s']=invoice_s
        context.update(InvoiceContext(request=request,invoice=invoice))
        return render(request,TEMPLATE_ROOT+"invoice-estelam.html",context)


class CategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        category_repo=CategoryRepo(request=request)
        category=category_repo.category(*args, **kwargs)
        context['category']=category
        category_s=json.dumps(CategorySerializer(category,many=False).data)
        context['category_s']=category_s 


        if category is None:
            categories=category_repo.roots()
            context['category_id']=0
            products=[]
        else:
            categories=category_repo.list(parent_id=category.id)
            products=category.products.order_by('priority')
            context['category_id']=category.id

        context['categories']=categories
        categories_s=json.dumps(CategorySerializer(categories,many=True).data)
        context['categories_s']=categories_s



        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s

        if request.user.has_perm(APP_NAME+'.add_category'):
            context['add_category_form']=AddCategoryForm()
            context['add_product_to_category_form']=AddProductToCategoryForm()
        if request.user.has_perm(APP_NAME+'.add_product'):
            context['add_product_form']=AddProductForm()
            context.update(AddProductContext(request=request))
        return render(request,TEMPLATE_ROOT+"category.html",context)


class CategoriesView(View):
    def get(self,request,*args, **kwargs):
        return CategoryView().get(request=request,pk=0)
      

class PersonAccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
       
        person_accounts=PersonAccountRepo(request=request).list(*args, **kwargs)

        context['person_accounts']=person_accounts
        person_accounts_s=json.dumps(PersonAccountSerializer(person_accounts,many=True).data)
        context['person_accounts_s']=person_accounts_s

        
        if request.user.has_perm(APP_NAME+'.add_personaccount'):
            context.update(AddPersonAccountContext(request=request))
            
        return render(request,TEMPLATE_ROOT+"person-accounts.html",context)

 

class BankAccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
       
        bank_accounts=BankAccountRepo(request=request).list(*args, **kwargs)

        context['bank_accounts']=bank_accounts
        bank_accounts_s=json.dumps(BankAccountSerializer(bank_accounts,many=True).data)
        context['bank_accounts_s']=bank_accounts_s

        
        if request.user.has_perm(APP_NAME+'.add_bankaccount'):
            context.update(AddBankAccountContext(request=request))
            
        return render(request,TEMPLATE_ROOT+"bank-accounts.html",context)


class BanksView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
       
        banks=BankRepo(request=request).list(*args, **kwargs)

        context['banks']=banks
        banks_s=json.dumps(BankSerializer(banks,many=True).data)
        context['banks_s']=banks_s

        
        if request.user.has_perm(APP_NAME+'.add_bank'):
            context.update(AddBankContext(request=request))
            
        return render(request,TEMPLATE_ROOT+"banks.html",context)


class BankAccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        bank_account=BankAccountRepo(request=request).bank_account(*args, **kwargs)
        context['bank_account']=bank_account

        if bank_account is None:
            raise Http404
        context.update(BankAccountContext(request=request,bank_account=bank_account))
        context.update(BankContext(request=request,bank=bank_account.bank))
         
        return render(request,TEMPLATE_ROOT+"bank-account.html",context)


class BankView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        bank=BankRepo(request=request).bank(*args, **kwargs)
        context['bank']=bank

        if bank is None:
            title='خطا'
            body='بانک مورد نظر پیدا نشد.'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context.update(BankContext(request=request,bank=bank))
        bank_accounts=BankAccountRepo(request=request).list(bank_id=bank.id)
        context['bank_accounts']=bank_accounts
        bank_accounts_s=json.dumps(BankAccountSerializer(bank_accounts,many=True).data)
        context['bank_accounts_s']=bank_accounts_s
        if request.user.has_perm(APP_NAME+'.add_bankaccount'):
            context.update(AddBankAccountContext(request=request,bank=bank))
        return render(request,TEMPLATE_ROOT+"bank.html",context)


class PersonAccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        person_account=PersonAccountRepo(request=request).person_account(*args, **kwargs)
        context['person_account']=person_account
 
        if person_account is None:
            title='خطا'
            body='حساب شخص پیدا نشد.'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context.update(PersonAccountContext(request=request,person_account=person_account))
         

        person_category=person_account.person_category
        context['person_category']=person_category
        person_category_s=json.dumps(PersonCategorySerializer(person_category).data)
        context['person_category_s']=person_category_s


        if request.user.has_perm(APP_NAME+'.add_bankaccount'):
            context.update(AddBankAccountContext(request=request,person=person_account.person))
        return render(request,TEMPLATE_ROOT+"person-account.html",context)


class PersonCategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        person_category=PersonCategoryRepo(request=request).person_category(*args, **kwargs)
        context['person_category']=person_category
        person_category_s=json.dumps(PersonCategorySerializer(person_category).data)
        context['person_category_s']=person_category_s


        person_category_account=person_category.account
        person_category_account_s=json.dumps(AccountBriefSerializer(person_category_account).data)
        context['person_category_account']=person_category_account
        context['person_category_account_s']=person_category_account_s
        
        


        person_accounts=person_category.personaccount_set.all()

        context['person_accounts']=person_accounts
        person_accounts_s=json.dumps(PersonAccountSerializer(person_accounts,many=True).data)
        context['person_accounts_s']=person_accounts_s

        if request.user.has_perm(APP_NAME+'.change_personcategory'):
            context['edit_person_category_form']=EditPersonCategoryForm()
            


        if request.user.has_perm(APP_NAME+'.add_personaccount'):
            context.update(AddPersonAccountContext(request=request))
            
        return render(request,TEMPLATE_ROOT+"person-category.html",context)


class PersonCategoriesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        person_categories=PersonCategoryRepo(request=request).list(*args, **kwargs)
        context['person_categories']=person_categories
        person_categories_s=json.dumps(PersonCategorySerializer(person_categories,many=True).data)
        context['person_categories_s']=person_categories_s
        if request.user.has_perm(APP_NAME+'.add_personcategory'):
            context.update(AddPersonCategoryContext(request=request))
        return render(request,TEMPLATE_ROOT+"person-categories.html",context)

    
class BrandView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        brand=BrandRepo(request=request).brand(*args, **kwargs)
        if brand is None:
            raise Http404
        
        context['brand']=brand
        products=brand.product_set.all()
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products']=products
        context['products_s']=products_s

        return render(request,TEMPLATE_ROOT+"brand.html",context)   


class BrandsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        brands=BrandRepo(request=request).list(*args, **kwargs)
        brands_s=json.dumps(BrandSerializer(brands,many=True).data)
        context['brands']=brands
        context['brands_s']=brands_s
        if request.user.has_perm(APP_NAME+'.add_brand'):
            context.update(AddBrandContext(request=request))
        return render(request,TEMPLATE_ROOT+"brands.html",context)


