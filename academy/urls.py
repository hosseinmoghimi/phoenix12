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
    path('teachers-excel/',login_required(views.TeachersExcelView.as_view()),name="teachers_excel"),
    path('import-teachers-from-excel/',login_required(apis.ImportTeachersFromExcelApi.as_view()),name="import_teachers_from_excel"),
    
    path('add-student-to-group/',login_required(views.AddStudentToGroupView.as_view()),name="add_student_to_group"),
    path('students/',login_required(views.StudentsView.as_view()),name="students"),
    path('student/<int:pk>/',login_required(views.StudentView.as_view()),name="student"),
    path('add-student/',login_required(apis.AddStudentApi.as_view()),name="add_student"),
    path('students-excel/',login_required(views.StudentsExcelView.as_view()),name="students_excel"),
    path('import-students-from-excel/',login_required(apis.ImportStudentsFromExcelApi.as_view()),name="import_students_from_excel"),

    
    path('sessions/',login_required(views.SessionsView.as_view()),name="sessions"),
    path('session/<int:pk>/',login_required(views.SessionView.as_view()),name="session"),
    path('add-session/',login_required(apis.AddSessionApi.as_view()),name="add_session"),

    path('majors/',login_required(views.MajorsView.as_view()),name="majors"),
    path('major/<int:pk>/',login_required(views.MajorView.as_view()),name="major"),
    path('add-major/',login_required(apis.AddMajorApi.as_view()),name="add_major"),


    path('schools/',login_required(views.SchoolsView.as_view()),name="schools"),
    path('school/<int:pk>/',login_required(views.SchoolView.as_view()),name="school"),
    path('add-school/',login_required(apis.AddSchoolApi.as_view()),name="add_school"),


    path('groups/',login_required(views.GroupsView.as_view()),name="groups"),
    path('group/<int:pk>/',login_required(views.GroupView.as_view()),name="group"),
    path('add-group/',login_required(apis.AddGroupApi.as_view()),name="add_group"),

    path('parents/',login_required(views.ParentsView.as_view()),name="parents"),
    path('parent/<int:pk>/',login_required(views.ParentView.as_view()),name="parent"),
    path('add-parent/',login_required(apis.AddParentApi.as_view()),name="add_parent"),
    path('set-students-for-parent/',login_required(apis.SetStudentsForParentApi.as_view()),name="set_students_for_parent"),


    path('add-attendance/',login_required(apis.AddAttendanceApi.as_view()),name="add_attendance"),


    path('educational_years/',login_required(views.EducationalYearsView.as_view()),name="educational_years"),
    path('educational_year/<int:pk>/',login_required(views.EducationalYearView.as_view()),name="educationalyear"),
    path('add-educational_year/',login_required(apis.AddEducationalYearApi.as_view()),name="add_educational_year"),


         
]
