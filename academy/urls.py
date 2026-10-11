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
    path('delete_all_words/',login_required(apis.DeleteAllWordsApi.as_view()),name='delete_all_words'),

    path('courses/',login_required(views.CoursesView.as_view()),name="courses"),
    path('course/<int:pk>/',login_required(views.CourseView.as_view()),name="course"),
    path('add-course/',login_required(apis.AddCourseApi.as_view()),name="add_course"),

    path('course_classes/',login_required(views.CourseClassesView.as_view()),name="course_classes"),
    path('course_class/<int:pk>/',login_required(views.CourseClassView.as_view()),name="courseclass"),
    path('add-course_class/',login_required(apis.AddCourseClassApi.as_view()),name="add_course_class"),

     
    path('words/',login_required(views.WordsView.as_view()),name="words"),
    path('word/<int:pk>/',login_required(views.WordView.as_view()),name="word"),
    path('add-word/',login_required(apis.AddWordApi.as_view()),name="add_word"),
    
    path('teachers/',login_required(views.TeachersView.as_view()),name="teachers"),
    path('teacher/<int:pk>/',login_required(views.TeacherView.as_view()),name="teacher"),
    path('add-teacher/',login_required(apis.AddTeacherApi.as_view()),name="add_teacher"),
    
    path('students/',login_required(views.StudentsView.as_view()),name="students"),
    path('student/<int:pk>/',login_required(views.StudentView.as_view()),name="student"),
    path('add-student/',login_required(apis.AddStudentApi.as_view()),name="add_student"),



    path('educational_years/',login_required(views.EducationalYearsView.as_view()),name="educational_years"),
    path('educational_year/<int:pk>/',login_required(views.EducationalYearView.as_view()),name="educationalyear"),
    path('add-educational_year/',login_required(apis.AddEducationalYearApi.as_view()),name="add_educational_year"),


         
]
