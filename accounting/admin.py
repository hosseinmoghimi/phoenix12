from django.contrib import admin
from .models import Category,FinancialYear,FinancialDocumentLine,FinancialDocument,PersonAccount
from .models import Account,FinancialEvent,InvoiceLineItemUnit,InvoiceLineItem 
from .models import Service,Product,Invoice,InvoiceLine,Bank,PersonCategory,Brand
from .models import BankAccount
from .models import ProductSpecification,Asset,Cheque


admin.site.register(Cheque)
admin.site.register(ProductSpecification)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(FinancialYear)
admin.site.register(FinancialDocument)
admin.site.register(FinancialDocumentLine)
admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(FinancialEvent)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
# admin.site.register(InvoiceLineItem)
admin.site.register(InvoiceLineItemUnit)
admin.site.register(PersonAccount)
admin.site.register(PersonCategory)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Asset)