from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('blogs/',login_required(views.BlogsView.as_view()),name="blogs"),  
    path('add-blog/',login_required(apis.AddBlogApi.as_view()),name="add_blog"),
    path('blog/<int:pk>/',login_required(views.BlogView.as_view()),name="blog"), 


    path('about/',login_required(views.BlogsView.as_view()),name="about"),  
    path('contact/',login_required(views.BlogsView.as_view()),name="contact"),  
    path('ourworks/',login_required(views.BlogsView.as_view()),name="ourworks"),  
     
]
