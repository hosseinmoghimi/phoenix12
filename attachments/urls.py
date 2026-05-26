from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),


    path('toggle-like/',apis.ToggleLikeApi.as_view(),name="toggle_like"),
 

    path('add-comment/',apis.AddCommentApi.as_view(),name="add_comment"),
    path('comments/',views.CommentsView.as_view(),name="comments"),
    path('delete-comment/',apis.DeleteCommentApi.as_view(),name="delete_comment"),
    
    path('add-page-print/',apis.AddPagePrintApi.as_view(),name="add_page_print"),


    path('add-link/',apis.AddLinkApi.as_view(),name="add_link"),
    path('links/',views.LinksView.as_view(),name="links"),


    path('add-download/',apis.AddDownloadApi.as_view(),name="add_download"),
    path('download/<int:pk>/',views.DownloadView.as_view(),name="download"),
    path('downloads/',views.DownloadsView.as_view(),name="downloads"),

    path('add-image/',apis.AddImageApi.as_view(),name="add_image"),
    path('image/<int:pk>/',views.ImageView.as_view(),name="image"),
    path('image/download/<int:pk>/',views.ImageDownloadView.as_view(),name="image_download"),
    path('images/',views.ImagesView.as_view(),name="images"),

    path('tag/<int:pk>/',views.TagView.as_view(),name='tag'),
    path('tags/',views.TagsView.as_view(),name='tags'),
    path('add_tag/',apis.AddTagApi.as_view(),name='add_tag'),

    
    path('location/<int:pk>/',views.LocationView.as_view(),name='location'),
    path('locations/',views.LocationsView.as_view(),name='locations'),
    path('add_location/',apis.AddLocationApi.as_view(),name='add_location'),
    path('add_page_location/',apis.AddPageLocationApi.as_view(),name='add_page_location'),

    path('areas/',views.AreasView.as_view(),name='areas'),
    path('area/<int:pk>/',views.AreaView.as_view(),name='area'),
    path('add_area/',apis.AddAreaApi.as_view(),name='add_area'),
]
