from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    path('search/',login_required(views.SearchView.as_view()),name="search"),  
    path('state/<int:pk>/',login_required(views.SearchView.as_view()),name="state"),  
    path('city/<int:pk>/',login_required(views.SearchView.as_view()),name="city"),  
    path('region/<int:pk>/',login_required(views.SearchView.as_view()),name="region"),  
    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),  
    path('pictures/',login_required(views.PicturesView.as_view()),name="pictures"), 
    path('parameters/',login_required(views.ParametersView.as_view()),name="parameters"), 
    path("get_parameters_and_pictures/",login_required(apis.GetParametersAndPicturesApi.as_view()),name="get_parameters_and_pictures"),
    path("set_parameter/",login_required(apis.SetParameterApi.as_view()),name="set_parameter"),
    path("download_db/",login_required(views.BackupDBView.as_view()),name="download_db"),
    path("download_media/",login_required(views.DownloadMediaView.as_view()),name="download_media"),
    path("download_privates/",login_required(views.DownloadPrivatesView.as_view()),name="download_privates"),

]

