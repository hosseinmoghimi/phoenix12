from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),  
    path('delete-all-foods/',login_required(apis.DeleteAllFoodsApi.as_view()),name="delete_all_foods"), 
    path('initial-default-foods/',login_required(apis.InitialDefaultFoodsApi.as_view()),name="initial_default_foods"), 
     
    path('add-food',login_required(apis.AddFoodApi.as_view()),name="add_food"), 
    path('food/<int:pk>/',login_required(views.FoodView.as_view()),name="food"),  
    path('foods/',login_required(views.FoodsView.as_view()),name="foods"),  
     

         
]
