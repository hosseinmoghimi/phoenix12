from django.urls import path
from .apps import APP_NAME
from . import views
app_name=APP_NAME
urlpatterns = [
    path("",views.IndexView.as_view(),name='home'),
    path("logs/",views.LogsView.as_view(),name='logs'),
    path("log/<int:pk>/",views.LogView.as_view(),name='log'),
]
