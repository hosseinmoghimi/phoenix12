from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",(views.HomeView.as_view()),name="home"),
    path("resumecategory/<int:pk>/",(views.ResumeCategoryView.as_view()),name="resumecategory"),
    path("resume/<int:pk>/",(views.ResumeIndexView.as_view()),name="resumeindex"),
    path("resume/<int:profile_id>/",(views.ResumeIndexView.as_view()),name="profile_resume_index"),
    # path('<int:profile_id>/',(views.HomeView.as_view()),name="resume_index2"),
    path("search/",(views.SearchView.as_view()),name="search"),
    # path("resume/<int:pk>/",(views.ResumeIndexView.as_view()),name="resume"),
 
    path('<int:profile_id>/<language_code>/',views.ResumeIndexView.as_view(),name="resume_index_language"),
    path('print/<int:pk>/',views.ResumePrint.as_view(),name="resume_print"),
    path('print/<int:pk>/<full>/',views.ResumePrint.as_view(),name="resume_print_full"),
    path('portfolio/<int:pk>/',views.PortfolioViews().portfolio,name="portfolio"),
    path('resume_fact/<int:pk>/',views.PortfolioViews().portfolio,name="resumefact"),
    path('resume_skill/<int:pk>/',views.PortfolioViews().portfolio,name="resumeskill"),
    # path('portfolio/<int:pk>/',views.BasicViews().portfolio,name="resumeportfolio"),
    path('service/<int:pk>/',views.ServiceViews().service,name="resumeservice"),
    path('resume/<int:pk>/',views.ResumeIndexView.as_view(),name="resume"),
    path('add_resume_item/',apis.BasicApi().add_resume_item,name="add_resume_item"),
    path('add_resume_fact/',apis.BasicApi().add_resume_fact,name="add_resume_fact"),
    path('add_resume_skill/',apis.BasicApi().add_resume_skill,name="add_resume_skill"),

    path('add_contact_message/',apis.BasicApi().add_contact_message,name="add_contact_message"),
]