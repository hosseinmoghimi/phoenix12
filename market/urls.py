from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('products/',login_required(views.ProductsView.as_view()),name="products"),
    path('cart/<int:customer_id>/',login_required(views.CartView.as_view()),name="cart"), 
    path('checkout_cart/',login_required(apis.CheckoutCartApi.as_view()),name="checkout_cart"), 
    path('product/<int:pk>/',login_required(views.ProductView.as_view()),name="product"), 
    path('shipper/<int:pk>/',login_required(views.ShipperView.as_view()),name="shipper"),
    path('shippers/',login_required(views.ShippersView.as_view()),name="shippers"),
    path('customers/',login_required(views.CustomersView.as_view()),name="customers"),
    path('customer/<int:pk>/',login_required(views.CustomerView.as_view()),name="customer"),
    path("add-shop/",login_required(apis.AddShopApi.as_view()),name="add_shop"),
    path("add-customer/",login_required(apis.AddCustomerApi.as_view()),name="add_customer"),
    path("add-shipper/",login_required(apis.AddShipperApi.as_view()),name="add_shipper"),
    path('shop/<int:pk>/',login_required(views.ProductView.as_view()),name="shop"),

    path('category/<int:pk>/',login_required(views.CategoryView.as_view()),name="category"),
    
    path('add-cart-item/',login_required(apis.AddCartItemApi.as_view()),name="add_cart_item"),

    path("change-cart-item/",login_required(apis.ChangeCartItemApi.as_view()),name="change_cart_item"),

    
    path("add-supplier/",login_required(apis.AddSupplierApi.as_view()),name="add_supplier"),
    path("suppliers/",login_required(views.SuppliersView.as_view()),name="suppliers"),
    path("supplier/<int:pk>/",(views.SupplierView.as_view()),name="supplier"),

    path("add-shop_package/",login_required(apis.AddShopPackageApi.as_view()),name="add_shop_package"),
    path("shop_packages/",login_required(views.ShopPackagesView.as_view()),name="shop_packages"),
    path("shop_package/<int:pk>/",(views.ShopPackageView.as_view()),name="shoppackage"),

]
