from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    path('add_invoice_to_project/',login_required(apis.AddInvoiceToProjectApi.as_view()),name="add_invoice_to_project"), 

    path('ticket/add/',login_required(apis.AddTicketApi.as_view()),name="add_ticket"),  
    path('tickets/',login_required(views.TicketsView.as_view()),name="tickets"),  
    path('ticket/<int:pk>/',login_required(views.TicketView.as_view()),name="ticket"),  

    path('add-event-to-project/',login_required(apis.AddEventToProjectApi.as_view()),name="add_event_to_project"),  

    path('project/add/sub/',login_required(apis.AddSubProjectApi.as_view()),name="add_sub_project"),  
    path('project/add/',login_required(apis.AddProjectApi.as_view()),name="add_project"),  
    path('projects/',login_required(views.ProjectsView.as_view()),name="projects"),  
    path('project/<int:pk>/',login_required(views.ProjectView.as_view()),name="project"),  
    path('project/edit/<int:pk>/',login_required(views.ProjectEditView.as_view()),name="project_edit"),  
    path("project_guantt/<int:pk>/",login_required(views.ProjectGuanttView.as_view()),name="project_guantt"),
    path('project/',login_required(views.ProjectView.as_view()),name="project_null"),  
    path('all-projects/',login_required(views.AllProjectsView.as_view()),name="all_projects"),
    path('normalize-project/',login_required(apis.NormalizeProjectApi.as_view()),name="normalize_project"),  
    path('edit-project/',login_required(apis.EditProjectApi.as_view()),name="edit_project"),  
    path('select-project/',login_required(apis.SelectProjectApi.as_view()),name="select_project"),
    
    path('add-project-invoice/',login_required(apis.AddProjectInvoiceApi.as_view()),name="add_project_invoice"),

    path('tree_chart/<int:pk>/',login_required(views.ProjectTreeChartView.as_view()),name="tree_chart"),  

    path('add-remote_client/',login_required(apis.AddRemoteClientApi.as_view()),name="add_remote_client"),  
    path('remote-clients/',login_required(views.RemoteClientsView.as_view()),name="remote_clients"),  
    path('remote-client/<int:pk>/',login_required(views.RemoteClientView.as_view()),name="remoteclient"),



   
]
