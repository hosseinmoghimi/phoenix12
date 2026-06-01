from utility.message import INVALID_FORM_VALUE_MESSAGE

from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from .repo import AssetRepo,CategoryRepo,BankRepo,PersonCategoryRepo,FinancialDocumentLineRepo,FinancialDocumentRepo,FinancialEventRepo,PersonAccountRepo,BrandRepo
from .repo import ServiceRepo,InvoiceRepo,InvoiceLineRepo,InvoiceLineItemUnitRepo,ProductRepo,AccountRepo,ChequeRepo
from utility.log import leolog
from .serializers import  InvoiceLineItemUnitBriefSerializer, ServiceSerializer,FinancialDocumentSerializer,FinancialEventSerializer,FinancialDocumentLineSerializer
from .serializers import CategorySerializer,InvoiceSerializer,InvoiceLineItemUnitSerializer,ProductSerializer,AccountSerializer,InvoiceLineSerializer,BrandSerializer
from .serializers import AssetSerializer,ChequeSerializer
from .serializers import BankAccountSerializer,BankSerializer
from .repo import BankAccountRepo
from django.http import JsonResponse
from .forms import *
from .repo import FinancialYearRepo,ProductSpecificationRepo,PersonAccountRepo
from .serializers import FinancialYearSerializer,ProductSpecificationSerializer,PersonAccountSerializer,PersonCategorySerializer
 
class AddProductToCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_product_to_category_form=AddProductToCategoryForm(request.POST)
        if add_product_to_category_form.is_valid():
            log=333
            cd=add_product_to_category_form.cleaned_data
            result,message,product_categories,product,category=CategoryRepo(request=request).add_product_to_category(**cd)
            if result==SUCCEED:
                context['product_categories']=CategorySerializer(product_categories,many=True).data
                context['category']=CategorySerializer(category,many=False).data
                context['product']=ProductSerializer(product,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddPersonAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_person_account_form=AddPersonAccountForm(request.POST)
        if add_person_account_form.is_valid():
            log=333
            cd=add_person_account_form.cleaned_data
            result,message,person_account=PersonAccountRepo(request=request).add_person_account(**cd)
            if result==SUCCEED:
                context['person_account']=PersonAccountSerializer(person_account,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class AddBankAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_bank_account_form=AddBankAccountForm(request.POST)
        if add_bank_account_form.is_valid():
            log=333
            cd=add_bank_account_form.cleaned_data
            result,message,bank_account=BankAccountRepo(request=request).add_bank_account(**cd)
            if result==SUCCEED:
                context['bank_account']=BankAccountSerializer(bank_account,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class AddBankApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_bank_form=AddBankForm(request.POST)
        if add_bank_form.is_valid():
            log=333
            cd=add_bank_form.cleaned_data
            result,message,bank=BankRepo(request=request).add_bank(**cd)
            if result==SUCCEED:
                context['bank']=BankSerializer(bank,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class AddPersonCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_person_category_form=AddPersonCategoryForm(request.POST)
        if add_person_category_form.is_valid():
            log=333
            cd=add_person_category_form.cleaned_data
            result,message,person_category=PersonCategoryRepo(request=request).add_person_category(**cd)
            if result==SUCCEED:
                context['person_category']=PersonCategorySerializer(person_category,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddProductSpecificationApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_product_specification_form=AddProductSpecificationForm(request.POST)
            if add_product_specification_form.is_valid():
                log=333
                cd=add_product_specification_form.cleaned_data 
                result,message,product_specification,deleted_id=ProductSpecificationRepo(request=request).add_product_specification(**cd)
                if product_specification is not None:
                    context['product_specification']=ProductSpecificationSerializer(product_specification).data
                    context['deleted_id']=deleted_id
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

class MergeProductApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            merge_product_form=MergeProductForm(request.POST)
            if merge_product_form.is_valid():
                log=333
                cd=merge_product_form.cleaned_data 
                result,message,merged_product=ProductRepo(request=request).merge_product(**cd)
                if merged_product is not None:
                    context['product']=ProductSerializer(merged_product).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class MergeAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            merge_account_form=MergeAccountForm(request.POST)
            if merge_account_form.is_valid():
                log=333
                cd=merge_account_form.cleaned_data 
                result,message,merged_account=AccountRepo(request=request).merge_account(**cd)
                if merged_account is not None:
                    context['account']=AccountSerializer(merged_account).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

class AddInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_invoice_form=AddInvoiceForm(request.POST)
        if add_invoice_form.is_valid():
            log=333
            cd=add_invoice_form.cleaned_data
            result,message,invoice=InvoiceRepo(request=request).add_invoice(**cd)
            if invoice is not None:
                context['invoice']=InvoiceSerializer(invoice).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddFinancialDocumentLineApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_financial_document_line_form=AddFinancialDocumentLineForm(request.POST)
        if add_financial_document_line_form.is_valid():
            log=333
            cd=add_financial_document_line_form.cleaned_data
            result,message,financial_document_line=FinancialDocumentLineRepo(request=request).add_financial_document_line(**cd)
            if financial_document_line is not None:

                context['financial_document_line']=FinancialDocumentLineSerializer(financial_document_line).data
                if cd['financial_document_id']==0:
                 context['financial_document']=FinancialDocumentSerializer(financial_document_line.financial_document).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        add_account_form=AddAccountForm(request.POST)
        if add_account_form.is_valid():
            cd=add_account_form.cleaned_data
            (result,message,account)=AccountRepo(request=request).add_account(**cd) 
            if result==SUCCEED:
                context["account"]=AccountSerializer(account).data
            # (result2,message2)=PersonRepo(request=request).initial_default_persons() 
        context['message']=message
        context['result']=result
        # context['message2']=message2
        # context['result2']=result2
        context['log']=log
        return JsonResponse(context)


class SetAccountParentApi(APIView): 
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        action=None
        log=111
        context['result']=FAILED
        set_parent_code_form=SetParentCodeForm(request.POST)
        if set_parent_code_form.is_valid():
            log=2222
            cd=set_parent_code_form.cleaned_data
            (result,message,account,parent)=AccountRepo(request=request).set_account_parent(**cd) 
            if result==SUCCEED:
                log=333 
                context["parent"]=AccountSerializer(parent,many=False).data 
                context["account"]=AccountSerializer(account,many=False).data 
        context['message']=message
        context['result']=result 
        context['log']=log
        return JsonResponse(context)


class AddInvoiceLineItemUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_invoice_line_item_unit_form=AddInvoiceLineItemUnitForm(request.POST)
            if add_invoice_line_item_unit_form.is_valid():
                log=333
                cd=add_invoice_line_item_unit_form.cleaned_data 
                result,message,invoice_line_item_units=InvoiceLineItemUnitRepo(request=request).add_invoice_line_item_unit(**cd)
                if invoice_line_item_units is not None:
                    context['invoice_line_item_units']=InvoiceLineItemUnitSerializer(invoice_line_item_units,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class ImportFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        
        message_products=''
        message_services=''
        message_accounts=''
        message_categories=''
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            import_from_excel_form=ImportFromExcelForm(request.POST,request.FILES)
            if import_from_excel_form.is_valid():
                log=333
                
                excel_file = request.FILES['file1']
                cd=import_from_excel_form.cleaned_data
                cd['excel_file']=excel_file
                result,message_categories,categories=CategoryRepo(request=request).import_categories_from_excel(**cd)
                result,message_products,products=ProductRepo(request=request).import_products_from_excel(**cd)
                result,message_services,services=ServiceRepo(request=request).import_services_from_excel(**cd)
                result,message_accounts,accounts=AccountRepo(request=request).import_accounts_from_excel(**cd)
                if categories is not None:
                    context['categories']=CategorySerializer(categories,many=True).data
                if products is not None:
                    context['products']=ProductSerializer(products,many=True).data
                if services is not None:
                    context['services']=ServiceSerializer(services,many=True).data
                if accounts is not None:
                    context['accounts']=AccountSerializer(accounts,many=True).data
        context['message_products']=message_products
        context['message_services']=message_services
        context['message_accounts']=message_accounts
        context['message_categories']=message_categories
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class ImportProductsFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            ImportProductsFromExcelForm_=ImportProductsFromExcelForm(request.POST,request.FILES)
            if ImportProductsFromExcelForm_.is_valid():
                log=333
                
                excel_file = request.FILES['file1']
                cd=ImportProductsFromExcelForm_.cleaned_data
                cd['excel_file']=excel_file
                result,message2,categories=CategoryRepo(request=request).import_categories_from_excel(**cd)
                result,message1,products=ProductRepo(request=request).import_products_from_excel(**cd)
                if products is not None:
                    context['products']=ProductSerializer(products,many=True).data
                if categories is not None:
                    context['categories']=CategorySerializer(categories,many=True).data
        context['message']=message1+"<br>"+message2
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class DeleteAllProductsApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            DeleteAllProductsForm_=DeleteAllProductsForm(request.POST)
            if DeleteAllProductsForm_.is_valid():
                log=333
                
                cd=DeleteAllProductsForm_.cleaned_data
                result,message=ProductRepo(request=request).delete_all()
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)





class DeleteAllCategoriesApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            DeleteAllCategoriesForm_=DeleteAllCategoriesForm(request.POST)
            if DeleteAllCategoriesForm_.is_valid():
                log=333
                cd=DeleteAllCategoriesForm_.cleaned_data
                result,message=CategoryRepo(request=request).delete_all()
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class ImportCategoriesFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            ImportCategoriesFromExcelForm_=ImportCategoriesFromExcelForm(request.POST,request.FILES)
            if ImportCategoriesFromExcelForm_.is_valid():
                log=333
                
                excel_file = request.FILES['file1']
                cd=ImportCategoriesFromExcelForm_.cleaned_data
                cd['excel_file']=excel_file
                result,message,categories=CategoryRepo(request=request).import_categories_from_excel(**cd) 
                if categories is not None:
                    context['categories']=CategorySerializer(categories,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class ImportServicesFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            ImportServicesFromExcelForm_=ImportServicesFromExcelForm(request.POST,request.FILES)
            if ImportServicesFromExcelForm_.is_valid():
                log=333
                
                excel_file = request.FILES['file1']
                cd=ImportServicesFromExcelForm_.cleaned_data
                cd['excel_file']=excel_file
                result,message,services=ServiceRepo(request=request).import_services_from_excel(**cd)
                if services is not None:
                    context['services']=ServiceSerializer(services,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddFinancialEventApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_financial_event_form=AddFinancialEventForm(request.POST,request.FILES)
            if add_financial_event_form.is_valid():
                log=333
                 
                cd=add_financial_event_form.cleaned_data
                result,message,financial_event=FinancialEventRepo(request=request).add_financial_event(**cd)
                if financial_event is not None:
                    context['financial_event']=FinancialEventSerializer(financial_event,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    

class AddChequeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_cheque_form=AddChequeForm(request.POST,request.FILES)
            if add_cheque_form.is_valid():
                log=333
                 
                cd=add_cheque_form.cleaned_data
                result,message,cheque=ChequeRepo(request=request).add_cheque(**cd)
                if cheque is not None:
                    context['cheque']=ChequeSerializer(cheque,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    
class AddInvoiceLineApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=INVALID_FORM_VALUE_MESSAGE
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_invoice_line_form=AddInvoiceLineForm(request.POST)
            if add_invoice_line_form.is_valid():
                log=333
                cd=add_invoice_line_form.cleaned_data 
                result,message,invoice_line=InvoiceLineRepo(request=request).add_invoice_line(**cd)
                if invoice_line is not None:
                    context['invoice_line']=InvoiceLineSerializer(invoice_line).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

 
class AddFinancialYearApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        add_financial_year_form=AddFinancialYearForm(request.POST)
        if add_financial_year_form.is_valid():
            cd=add_financial_year_form.cleaned_data
            (result,message,financial_year,financial_years)=FinancialYearRepo(request=request).add_financial_year(**cd) 
            if result==SUCCEED:
                context["financial_years"]=FinancialYearSerializer(financial_years,many=True).data
                context["financial_year"]=FinancialYearSerializer(financial_year).data
            # (result2,message2)=PersonRepo(request=request).initial_default_persons() 
        context['message']=message
        context['result']=result
        # context['message2']=message2
        # context['result2']=result2
        context['log']=log
        return JsonResponse(context)
 

class SetAccountParentApi(APIView): 
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        action=None
        log=111
        context['result']=FAILED
        set_parent_code_form=SetParentCodeForm(request.POST)
        if set_parent_code_form.is_valid():
            log=2222
            cd=set_parent_code_form.cleaned_data
            (result,message,account,parent)=AccountRepo(request=request).set_account_parent(**cd) 
            if result==SUCCEED:
                log=333 
                context["parent"]=AccountSerializer(parent,many=False).data 
                context["account"]=AccountSerializer(account,many=False).data 
        context['message']=message
        context['result']=result 
        context['log']=log
        return JsonResponse(context)


class GetInvoiceLineItemUnitsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            get_invoice_line_item_units_form=GetInvoiceLineItemUnitsForm(request.POST)
            if get_invoice_line_item_units_form.is_valid():
                log=333
                cd=get_invoice_line_item_units_form.cleaned_data 
                invoice_line_item_units=InvoiceLineItemUnitRepo(request=request).list(**cd)
                if invoice_line_item_units is not None:
                    context['invoice_line_item_units']=InvoiceLineItemUnitBriefSerializer(invoice_line_item_units,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    

class EditFinancialEventApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            edit_financial_event_form=EditFinancialEventForm(request.POST)
            if edit_financial_event_form.is_valid():
                log=333
                cd=edit_financial_event_form.cleaned_data
                result,message,financial_event=FinancialEventRepo(request=request).edit_financial_event(**cd)
                if financial_event is not None:
                    context['financial_event']=FinancialEventSerializer(financial_event).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class EditFinancialDocumentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            edit_financial_document_form=EditFinancialDocumentForm(request.POST)
            if edit_financial_document_form.is_valid():
                log=333
                cd=edit_financial_document_form.cleaned_data
                result,message,financial_document=FinancialDocumentRepo(request=request).edit_financial_document(**cd)
                if financial_document is not None:
                    context['financial_document']=FinancialDocumentSerializer(financial_document).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)





class EditFinancialDocumentLineApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            edit_financial_document_line_form=EditFinancialDocumentLineForm(request.POST)
            if edit_financial_document_line_form.is_valid():
                log=333
                cd=edit_financial_document_line_form.cleaned_data
                result,message,financial_document_line=FinancialDocumentLineRepo(request=request).edit_financial_document_line(**cd)
                if financial_document_line is not None:
                    context['financial_document_line']=FinancialDocumentLineSerializer(financial_document_line).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class SelectFinancialEventApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_financial_event_form=SelectFinancialEventForm(request.POST)
            if select_financial_event_form.is_valid():
                log=333
                cd=select_financial_event_form.cleaned_data
                financial_event=FinancialEventRepo(request=request).financial_event(**cd)
                if financial_event is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['financial_event']=FinancialEventSerializer(financial_event).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class SelectFinancialDocumentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_financial_document_form=SelectFinancialDocumentForm(request.POST)
            if select_financial_document_form.is_valid():
                log=333
                cd=select_financial_document_form.cleaned_data
                financial_document=FinancialDocumentRepo(request=request).financial_document(**cd)
                if financial_document is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['financial_document']=FinancialDocumentSerializer(financial_document).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
 
class SelectAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_account_form=SelectAccountForm(request.POST)
            if select_account_form.is_valid():
                log=333
                cd=select_account_form.cleaned_data
                account=AccountRepo(request=request).account(**cd)
                if account is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['account']=AccountSerializer(account).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class EditPersonCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            edit_person_category_form=EditPersonCategoryForm(request.POST)
            if edit_person_category_form.is_valid():
                log=333
                cd=edit_person_category_form.cleaned_data
                result,message,person_category=PersonCategoryRepo(request=request).edit_person_category(**cd)
                if result==SUCCEED:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['person_category']=PersonCategorySerializer(person_category).data
                    context['account']=AccountSerializer(person_category.account).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class SelectPersonAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_person_account_form=SelectPersonAccountForm(request.POST)
            if select_person_account_form.is_valid():
                log=333
                cd=select_person_account_form.cleaned_data
                person_account=PersonAccountRepo(request=request).person_account(**cd)
                if person_account is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['person_account']=PersonAccountSerializer(person_account).data
                    context['account']=AccountSerializer(person_account).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

        
class SelectProductApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_product_form=SelectProductForm(request.POST)
            if select_product_form.is_valid():
                log=333
                cd=select_product_form.cleaned_data
                product_repo=ProductRepo(request=request)
                
                if cd['barcode'] is not None and len(cd['barcode'])>0:
                    product=product_repo.product(barcode=cd['barcode'])
                    context['product']=ProductSerializer(product).data
                
                if cd['id'] is not None and cd['id']>0:
                    product=product_repo.product(id=cd['id'])
                    context['product']=ProductSerializer(product).data

                if 'title' in cd:
                    title=cd['title']
                    if len(title)>0:
                        products=product_repo.list(title=title)
                        context['products']=ProductSerializer(products,many=True).data
                 
                result=SUCCEED
                message="موفقیت آمیز"
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    

class InitAllAccountsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            (result1,message1)=AccountRepo(request=request).initial_default_accounts() 
            (result2,message2)=PersonCategoryRepo(request=request).initial_default_person_categories()
            (result3,message3)=BankRepo(request=request).initial_default_banks() 
        context['message1']=message1
        context['result1']=result1
        context['message2']=message2
        context['result2']=result2
        context['message3']=message3
        context['result3']=result3
        context['log']=log
        return JsonResponse(context)




class NormalizeAllAccountsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        counter=0
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            (result,message,counter)=AccountRepo(request=request).normalize_all_accounts() 
        context['counter']=counter
        context['message']=message
        context['result']=result 
        context['log']=log
        return JsonResponse(context)
    
    
class NormalizeAllFinancialDocumentsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        counter=0
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            (result,message,counter)=FinancialDocumentRepo(request=request).normalize_all_financial_documents() 
        context['counter']=counter
        context['message']=message
        context['result']=result 
        context['log']=log
        return JsonResponse(context)



class DeleteAllAccountsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            from authentication.repo import PersonRepo
            (result2,message2)=PersonCategoryRepo(request=request).delete_all() 
            (result3,message3)=PersonRepo(request=request).delete_all() 
            (result3,message3)=FinancialDocumentLineRepo(request=request).delete_all() 
            (result3,message3)=FinancialEventRepo(request=request).delete_all() 
            (result3,message3)=PersonAccountRepo(request=request).delete_all() 
            (result,message)=AccountRepo(request=request).delete_all_accounts() 
            (result2,message2)=BankRepo(request=request).delete_all() 
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class EditInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
         
        edit_invoice_form=EditInvoiceForm(request.POST)
        if edit_invoice_form.is_valid():
            log=333
            cd=edit_invoice_form.cleaned_data
            if 'invoice_lines' in cd and cd['invoice_lines'] is not None and not cd['invoice_lines']=='':
                cd['invoice_lines']=json.loads(cd['invoice_lines'])
            result,message,invoice=InvoiceRepo(request=request).edit_invoice(**cd)
            if invoice is not None:
                context['invoice']=InvoiceSerializer(invoice).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddBrandApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_brand_form=AddBrandForm(request.POST)
        if add_brand_form.is_valid():
            log=333
            cd=add_brand_form.cleaned_data
            result,message,brand=BrandRepo(request=request).add_brand(**cd)
            if brand is not None:
                context['brand']=BrandSerializer(brand).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddAssetApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_asset_form=AddAssetForm(request.POST)
        if add_asset_form.is_valid():
            log=333
            cd=add_asset_form.cleaned_data
            result,message,asset=AssetRepo(request=request).add_asset(**cd)
            if asset is not None:
                context['asset']=AssetSerializer(asset).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddProductApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_product_form=AddProductForm(request.POST)
        if add_product_form.is_valid():
            log=333
            cd=add_product_form.cleaned_data
            result,message,product=ProductRepo(request=request).add_product(**cd)
            if product is not None:
                context['product']=ProductSerializer(product).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    
class GetReportApi(APIView):
    def post(self,request,*args, **kwargs):

        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        get_report_form=GetReportForm(request.POST)
        if get_report_form.is_valid():
            log=333
            cd=get_report_form.cleaned_data
            result=SUCCEED
            financial_document_lines=FinancialDocumentLineRepo(request=request).list(**cd)
            context['financial_document_lines']=FinancialDocumentLineSerializer(financial_document_lines,many=True).data
            financial_events=FinancialEventRepo(request=request).list(**cd)
            context['financial_events']=FinancialEventSerializer(financial_events,many=True).data

        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

class AddServiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_service_form=AddServiceForm(request.POST)
        if add_service_form.is_valid():
            log=333
            cd=add_service_form.cleaned_data
            result,message,service=ServiceRepo(request=request).add_service(**cd)
            if service is not None:
                context['service']=ServiceSerializer(service).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class AddCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        add_category_form=AddCategoryForm(request.POST)
        if add_category_form.is_valid():
            log=333
            cd=add_category_form.cleaned_data
            result,message,category=CategoryRepo(request=request).add_category(**cd)
            if category is not None:
                context['category']=CategorySerializer(category).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 