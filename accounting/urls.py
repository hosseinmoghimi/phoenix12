from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),

    path("help/",login_required(views.HelpView.as_view()),name="help"),
    path("tree-chart/<int:pk>/",login_required(views.TreeChartView.as_view()),name="tree_chart"),
    path("tree-list/",login_required(views.TreeListView.as_view()),name="tree_list"),
    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),
    path("normalize_all_financial_documents/",login_required(apis.NormalizeAllFinancialDocumentsApi.as_view()),name="normalize_all_financial_documents"),
    path("normalize_all_accounts/",login_required(apis.NormalizeAllAccountsApi.as_view()),name="normalize_all_accounts"),

    path("init_all_accounts/",login_required(apis.InitAllAccountsApi.as_view()),name="init_all_accounts"),
    path("delete_all_accounts/",login_required(apis.DeleteAllAccountsApi.as_view()),name="delete_all_accounts"),
    
    path("person/<int:pk>/",login_required(views.PersonView.as_view()),name="person"), 

    
    path("financial-year/<int:pk>/",login_required(views.FinancialYearView.as_view()),name="financialyear"),
    path("financial-years/",login_required(views.FinancialYearsView.as_view()),name="financial_years"),
    path("add-financial-year/",login_required(apis.AddFinancialYearApi.as_view()),name="add_financial_year"),
    
    path('person-category/<int:pk>/',login_required(views.PersonCategoryView.as_view()),name="personcategory"),
    path('person-categories/',login_required(views.PersonCategoriesView.as_view()),name="person_categories"),

    path('person-accounts/',login_required(views.PersonAccountsView.as_view()),name="person_accounts"),
    path('person-account/<int:pk>/',login_required(views.PersonAccountView.as_view()),name="personaccount"),
    path("add-person-account/",login_required(apis.AddPersonAccountApi.as_view()),name="add_person_account"),
    path("add-person-category/",login_required(apis.AddPersonCategoryApi.as_view()),name="add_person_category"),
    path("edit-person-category/",login_required(apis.EditPersonCategoryApi.as_view()),name="edit_person_category"),
    path("select-person-account/",login_required(apis.SelectPersonAccountApi.as_view()),name="select_person_account"),
    
    path("get-invoice-line-item-units/",login_required(apis.GetInvoiceLineItemUnitsApi.as_view()),name="get_invoice_line_item_units"),
    
    path("add-bank-account/",login_required(apis.AddBankAccountApi.as_view()),name="add_bank_account"),
    path('bank-accounts/',login_required(views.BankAccountsView.as_view()),name="bank_accounts"),
    path('bank-account/<int:pk>/',login_required(views.BankAccountView.as_view()),name="bankaccount"),



    path("add-bank/",login_required(apis.AddBankApi.as_view()),name="add_bank"),
    path('banks/',login_required(views.BanksView.as_view()),name="banks"),
    path('bank/<int:pk>/',login_required(views.BankView.as_view()),name="bank"),

    path('accounts/',login_required(views.AccountsView.as_view()),name="accounts"),
    path('account/<int:pk>/',login_required(views.AccountView.as_view()),name="account"),
    path("add-account/",login_required(apis.AddAccountApi.as_view()),name="add_account"),
    path("select-account/",login_required(apis.SelectAccountApi.as_view()),name="select_account"),
    path('selection/',login_required(views.SelectionView.as_view()),name="selection"),
    path("set_account_parent/",login_required(apis.SetAccountParentApi.as_view()),name="set_account_parent"),

    path('financial-documents/',login_required(views.FinancialDocumentsView.as_view()),name="financial_documents"),
    path('financial-document/<int:pk>/',login_required(views.FinancialDocumentView.as_view()),name="financialdocument"),
    path("select-financial-document/",login_required(apis.SelectFinancialDocumentApi.as_view()),name="select_financial_document"),
    path("edit-financial-document/",login_required(apis.EditFinancialDocumentApi.as_view()),name="edit_financial_document"),
    
    path('financial-document-lines/',login_required(views.FinancialDocumentLinesView.as_view()),name="financial_document_lines"),
    path('financial-document-lines-print/',login_required(views.FinancialDocumentLinesPrintView.as_view()),name="financial_document_lines_print"),
    path('financial-document-line/<int:pk>/',login_required(views.FinancialDocumentLineView.as_view()),name="financialdocumentline"),
    path('add-financial-document-line/',login_required(apis.AddFinancialDocumentLineApi.as_view()),name="add_financial_document_line"),
    path("edit-financial-document-line/",login_required(apis.EditFinancialDocumentLineApi.as_view()),name="edit_financial_document_line"),
    
    path('brands/',login_required(views.BrandsView.as_view()),name="brands"),
    path('brand/<int:pk>/',login_required(views.BrandView.as_view()),name="brand"),
    path("add-brand/",login_required(apis.AddBrandApi.as_view()),name="add_brand"),

    path('cheques/',login_required(views.ChequesView.as_view()),name="cheques"),
    path('cheque/<int:pk>/',login_required(views.ChequeView.as_view()),name="cheque"),
    path("add-cheque/",login_required(apis.AddChequeApi.as_view()),name="add_cheque"),

    
    path('products/',login_required(views.ProductsView.as_view()),name="products"),
    path('product/<int:pk>/',login_required(views.ProductView.as_view()),name="product"),
    path("add-product/",login_required(apis.AddProductApi.as_view()),name="add_product"),
    path("select-product/",login_required(apis.SelectProductApi.as_view()),name="select_product"),


    path('export-to-excel/',login_required(views.ExportToExcelView.as_view()),name="export_to_excel"),
    path("import-from-excel/",login_required(apis.ImportFromExcelApi.as_view()),name="import_from_excel"),
    path('export-categories-to-excel/',login_required(views.ExportCategoriesToExcelView.as_view()),name="export_categories_to_excel"),
    path('export-products-to-excel/',login_required(views.ExportProductsToExcelView.as_view()),name="export_products_to_excel"),
    path("import-products-from-excel/",login_required(apis.ImportProductsFromExcelApi.as_view()),name="import_products_from_excel"),
    path("import-categories-from-excel/",login_required(apis.ImportCategoriesFromExcelApi.as_view()),name="import_categories_from_excel"),
    
    path("delete-all-products/",login_required(apis.DeleteAllProductsApi.as_view()),name="delete_all_products"),
    path("delete-all-categories/",login_required(apis.DeleteAllCategoriesApi.as_view()),name="delete_all_categories"),
    
    path('export-services-to-excel/',login_required(views.ExportServicesToExcelView.as_view()),name="export_services_to_excel"),
    path("import-services-from-excel/",login_required(apis.ImportServicesFromExcelApi.as_view()),name="import_services_from_excel"),
    
    
    path('add-product-to-category/',login_required(apis.AddProductToCategoryApi.as_view()),name="add_product_to_category"),
    
    path('invoices/',login_required(views.InvoicesView.as_view()),name="invoices"),
    path('invoice/<int:pk>/',login_required(views.InvoiceView.as_view()),name="invoice"),
    path('new_invoice/',login_required(views.NewInvoiceView.as_view()),name="new_invoice"),
    path('invoice/no/<int:invoice_no>/',login_required(views.InvoiceView.as_view()),name="invoice_no"),
    path('invoice/edit/<int:pk>/',login_required(views.InvoiceEditView.as_view()),name="invoice_edit"),
    path('invoice/excel/<int:pk>/',login_required(views.InvoiceToExcelView.as_view()),name="invoice_to_excel"),
    path('invoice-line-item/<int:pk>/',login_required(views.InvoiceLineItemView.as_view()),name="invoicelineitem"),
    path('invoice/print/<int:pk>/',login_required(views.InvoicePrintView.as_view()),name="invoice_print"),
    path('invoice-estelam/<int:pk>/',login_required(views.InvoiceEstelamView.as_view()),name="invoice_estelam"),
    path('invoice-official-print/<int:pk>/',login_required(views.InvoiceOfficialPrintView.as_view()),name="invoice_official_print"),
    path('invoice_line/<int:pk>/',login_required(views.InvoiceLineView.as_view()),name="invoiceline"),

    
    path('categories/',login_required(views.CategoriesView.as_view()),name="categories"),
    path('category/<int:pk>/',login_required(views.CategoryView.as_view()),name="category"),
    path("add-category/",login_required(apis.AddCategoryApi.as_view()),name="add_category"),



    path("add-product-specification/",login_required(apis.AddProductSpecificationApi.as_view()),name="add_product_specification"),
    path("merge-product/",login_required(apis.MergeProductApi.as_view()),name="merge_product"),
    path("report/",login_required(views.ReportView.as_view()),name="report"),

     
    path("merge-account/",login_required(apis.MergeAccountApi.as_view()),name="merge_account"),

    path('assets/',login_required(views.AssetsView.as_view()),name="assets"),
    path('asset/<int:pk>/',login_required(views.AssetView.as_view()),name="asset"),
    path("add-asset/",login_required(apis.AddAssetApi.as_view()),name="add_asset"),
    
    path('services/',login_required(views.ServicesView.as_view()),name="services"),
    path('service/<int:pk>/',login_required(views.ServiceView.as_view()),name="service"),
    path("add-service/",login_required(apis.AddServiceApi.as_view()),name="add_service"),
 
    path('add-invoice/',login_required(views.AddInvoiceView.as_view()),name="add_invoice"),
    path("add-invoice-line/",login_required(apis.AddInvoiceLineApi.as_view()),name="add_invoice_line"),
    
    path("add-invoice-line-item-unit/",login_required(apis.AddInvoiceLineItemUnitApi.as_view()),name="add_invoice_line_item_unit"),
    path("edit-invoice/",login_required(apis.EditInvoiceApi.as_view()),name="edit_invoice"),

    path("change-cheque-image/",login_required(views.ChangeChequeImageView.as_view()),name="change_cheque_image"),

    path("make-financial-event-draft/",login_required(views.MakeFinancialEventDraftView.as_view()),name="make_financial_event_draft"),
      
    path("financial-events/",login_required(views.FinancialEventsView.as_view()),name="financial_events"),
    path("new-financial-event/",login_required(views.NewFinancialEventView.as_view()),name="new_financial_event"),
    
    path("financial-event/<int:pk>/",login_required(views.FinancialEventView.as_view()),name="financialevent"),
    path("add-financial-event/",login_required(apis.AddFinancialEventApi.as_view()),name="add_financial_event"),
    path("select-financial-event/",login_required(apis.SelectFinancialEventApi.as_view()),name="select_financial_event"),
    path("edit-financial-event/",login_required(apis.EditFinancialEventApi.as_view()),name="edit_financial_event"),
    
    
    path("set_account_parent/",login_required(apis.SetAccountParentApi.as_view()),name="set_account_parent"),



   

    
]
