from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",views.IndexView.as_view(),name='home'),
    path("drugs/",views.DrugsView.as_view(),name='drugs'),
    path("drug/<int:pk>/",views.DrugView.as_view(),name='drug'),
]
