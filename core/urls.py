from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('coming-soon/',login_required(views.ComingSoonView.as_view()),name="comingsoon"),
    path('search/',login_required(views.SearchView.as_view()),name="search"),
    path('toggle-like/',apis.TogglePageLikeApi.as_view(),name="toggle_like"),
    path('page/<int:pk>/',views.PageView.as_view(),name="page"),
    path('event/<int:pk>/',views.EventView.as_view(),name="event"),
    path('set-page-thumbnail-header/',apis.SetPageThumbnailHeaderApi.as_view(),name="set_page_thumbnail_header"),
    path('set-page-priority/',apis.SetPagePriorityApi.as_view(),name="set_page_priority"),
    path('add_related_page/',apis.AddRelatedPageApi.as_view(),name="add_related_page"),

]
