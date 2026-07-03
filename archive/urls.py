from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.HomeView.as_view()),name='home'),
    path('search/',login_required(views.SearchView.as_view()),name='search'),
    path('file/<int:pk>/',login_required(views.FileView.as_view()),name='file'),
    path('folder/<int:pk>/',login_required(views.FolderView.as_view()),name='folder'),
    path('open_folder/',login_required(apis.OpenFolderApi.as_view()),name='open_folder'),
    path('create_folder/',login_required(views.CreateFolderApi.as_view()),name='create_folder'),
    path('create_file/',login_required(views.CreateFileApi.as_view()),name='create_file'),
]
