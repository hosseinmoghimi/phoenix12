import logging
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
from bms.apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.HomeView.as_view()),name='home'),
    path('feeders/',login_required(views.FeedersView.as_view()),name='feeders'),
    path('log/<int:pk>/',login_required(views.LogView.as_view()),name='log'),
    path('logs/',login_required(views.LogsView.as_view()),name='logs'),
    path('feeder/<int:pk>/',login_required(views.FeederView.as_view()),name='feeder'),
    path('relay/<int:pk>/',login_required(views.FeedersView.as_view()),name='relay'),
    path('command/<int:pk>/',login_required(views.FeedersView.as_view()),name='command'),
    path('commands/',login_required(views.CommandsView.as_view()),name='commands'),
    path('scenario/<int:pk>/',login_required(views.FeedersView.as_view()),name='scenario'),
    
    path('export/',login_required(apis.ExportApi.as_view()),name="export"),
    path('execute_command/',login_required(apis.ExecuteCommandApi.as_view()),name="execute_command"),
    path('add_log_from_client/',login_required(apis.ExportApi.as_view()),name="add_log_from_client"),
]
