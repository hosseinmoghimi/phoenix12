from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
     
    path('add-food',login_required(apis.AddFoodApi.as_view()),name="add_food"), 
    path('food/<int:pk>/',login_required(views.FoodView.as_view()),name="food"),  
    path('foods/',login_required(views.FoodsView.as_view()),name="foods"),  
     

         
]
