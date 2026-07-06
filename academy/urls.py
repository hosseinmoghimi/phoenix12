from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    path('search/',login_required(views.SearchView.as_view()),name="search"),  
    

    
    path('settings/',login_required(views.SettingsView.as_view()),name='settings'),
    path('get-json-backup/',login_required(views.GetJsonBackupView.as_view()),name='get_json_backup'),
    path('import_from_json/',login_required(apis.ImportFromJsonApi.as_view()),name='import_from_json'),

    path('courses/',login_required(views.CoursesView.as_view()),name="courses"),
    path('course/<int:pk>/',login_required(views.CourseView.as_view()),name="course"),
    path('add-course/',login_required(apis.AddCourseApi.as_view()),name="add_course"),

     
    path('words/',login_required(views.WordsView.as_view()),name="words"),
    path('word/<int:pk>/',login_required(views.WordView.as_view()),name="word"),
    path('add-word/',login_required(apis.AddWordApi.as_view()),name="add_word"),


         
]
