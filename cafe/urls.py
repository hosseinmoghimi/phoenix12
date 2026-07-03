from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    
    path('checkout-cart',login_required(apis.CheckoutCartApi.as_view()),name="checkout_cart"), 
   
    path('add-table',login_required(apis.AddTableApi.as_view()),name="add_table"), 
    path('table/<int:pk>/',login_required(views.TableView.as_view()),name="table"),  
    path('tables/',login_required(views.TablesView.as_view()),name="tables"),  
    
    path('order/',login_required(views.OrderView.as_view()),name="order"),

    path('graph/',login_required(views.GraphView.as_view()),name="graph"),
    path('graph2/',login_required(views.Graph2View.as_view()),name="graph2"),
    path('menus/',login_required(views.MenusView.as_view()),name="menus"),
    path('menu/<int:pk>/',login_required(views.MenuView.as_view()),name="menu"),
    path('add-menu/',login_required(apis.AddMenuApi.as_view()),name="add_menu"),


    
    path('orders/',login_required(views.MenusView.as_view()),name="orders"),
    path('order/<int:pk>/',login_required(views.MenuView.as_view()),name="order"),
    path('add-order/',login_required(apis.AddMenuApi.as_view()),name="add_order"),

         
]
