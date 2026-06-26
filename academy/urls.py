from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    
    path('courses/',login_required(views.CoursesView.as_view()),name="courses"),
    path('course/<int:pk>/',login_required(views.CourseView.as_view()),name="course"),
    path('add-course/',login_required(apis.AddCourseApi.as_view()),name="add_course"),

         
]
