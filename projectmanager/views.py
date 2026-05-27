from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from utility.enums import *
from .serializers import ProjectSerializer,RemoteClientSerializer,TicketWithChildrenSerializer,ProjectSerializerForGuantt,TicketSerializer
from .repo import ProjectRepo,RemoteClientRepo,TicketRepo
from organization.views import OrganizationalUnitRepo,OrganizationalUnitSerializer
from .apps import APP_NAME
from core.views import CoreContext,PageContext,MessageView
from utility.calendar import PersianCalendar
from utility.currency import to_price
import json
from utility.enums import UnitNameEnum
from utility.views import NoPersmissionView
from utility.log import leolog
from accounting.views import ProductContext,PageContext,AddInvoiceContext,InvoiceSerializer,InvoiceLineWithInvoiceSerializer
from core.views import EventSerializer
from .enums import *
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='projectmanager/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def TicketContext(request,ticket,*args, **kwargs):
    context={}
    context['ticket']=ticket
    ticket_s=json.dumps(TicketSerializer(ticket).data)
    context['ticket_s']=ticket_s


    tickets=TicketRepo(request=request).list(parent_id=ticket.id)
    context['tickets']=tickets
    tickets_s=json.dumps(TicketWithChildrenSerializer(tickets,many=True).data)
    context['tickets_s']=tickets_s


    project=ticket.project
    context['project']=project
    project_s=json.dumps(ProjectSerializer(project).data)
    context['project_s']=project_s
    context.update(AddTicketContext(request=request))
    return context

def AddTicketContext(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_ticket"):
        context['add_ticket_form']=AddTicketForm() 
    return context

def ProjectContext(request,project,*args, **kwargs):
    context=PageContext(request=request,page=project)
    context['project']=project
    project_s=json.dumps(ProjectSerializer(project).data)


    projects=project.children.filter(class_name=project.class_name).order_by('priority')
    context['projects']=projects
    projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
    context['projects_s']=projects_s
    if request.user.has_perm(APP_NAME+'.add_project'):
        context['add_sub_project_form']=AddSubProjectForm()
    context['project_s']=project_s
    context['WIDE_LAYOUT']=True

    if request.user.has_perm(APP_NAME+'.change_project'):
        context['edit_project_form']=EditProjectForm()
        context['colors_for_change_project']=(i[0] for i in ColorEnum.choices)
        all_organizational_units=OrganizationalUnitRepo(request=request).list()
        context['all_organizational_units']=all_organizational_units
        
        context['project_status_enum'] = (i[0] for i in ProjectStatusEnum.choices)
    return context


def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False
    

    projects=ProjectRepo(request=request).list(search_for=search_for)
    if len(projects)>0:
        context['projects']=projects
        context['projects_s']=json.dumps(ProjectSerializer(projects,many=True).data)
        WAS_FOUND=True


    remote_clients=RemoteClientRepo(request=request).list(search_for=search_for)
    if len(remote_clients)>0:
        context['remote_clients']=remote_clients
        context['remote_clients_s']=json.dumps(RemoteClientSerializer(remote_clients,many=True).data)
        WAS_FOUND=True


    context['WAS_FOUND']=WAS_FOUND
    return context



class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps



        
        projects = ProjectRepo(request=request).list(parent_id=None,*args, **kwargs)
        # context['expand_projects']=True
        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s

        return render(request,TEMPLATE_ROOT+"index.html",context)


class ProjectGuanttView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return NoPersmissionView(request=request)
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context['project'] = project
        projects=ProjectRepo(request=request).list(parent_id=project.pk).order_by('priority')
        context['projects'] = projects
        context['projects_s'] = json.dumps(ProjectSerializerForGuantt(projects, many=True).data)
        return render(request, TEMPLATE_ROOT+"guantt.html", context)


class ProjectTreeChartView(View):
    
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        if project is None:
            title='پروژه وجود ندارد'
            body='پروژه وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context['project']=project  


        projects=project.all_sub_projects()
        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s

        
        context['WIDE_LAYOUT']=True 
         
        
        pages=[{
                'title': f"""{project.title}""",
                'parent_id': project.parent_id,
                'parent': 0,
                'get_absolute_url': project.get_absolute_url(),
                'id': project.id,
                'pre_title': "",
                'color': project.color,
                'sub_title':to_price(project.total_price),
                }]
          
        for project in projects:
            pages.append({
                'title': f"""{project.title}""",
                'parent_id': project.parent_id,
                'parent': 0,
                'get_absolute_url': project.get_absolute_url(),
                'id': project.id,
                'pre_title': "",
                'color': project.color,
                'sub_title':to_price(project.amount),
                })

        context['pages_s'] = json.dumps(pages)
        return render(request,TEMPLATE_ROOT+"tree-chart.html",context) 


class ProjectView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        # project.normalize()
        if project is None:
            title='پروژه وجود ندارد'
            body='پروژه وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context.update(ProjectContext(request=request,project=project))

        all_sub_ids=project.all_sub_ids(same_class=True,my_id=True)


        
        invoices=project.invoices.order_by('-event_datetime')
        invoices=project.all_invocie().order_by('-event_datetime')
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s




        
        invoice_lines=project.all_invocie_lines().order_by('row').order_by('invoice_id')
        invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s



        events=project.events.order_by('-event_datetime')
        events_s=json.dumps(EventSerializer(events,many=True).data)
        context['events']=events
        context['events_s']=events_s
        if request.user.has_perm('core.add_event'):
            context['add_event_to_project_form']=AddEventToProjectForm()


        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".add_invoice"):
            context.update(AddInvoiceContext(request=request))


            

        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".change_project"):
            context['add_invoice_to_project_form']=AddInvoiceToProjectForm()

        tickets=TicketRepo(request=request).list(project_id__in=all_sub_ids)
        context['tickets']=tickets
        tickets_s=json.dumps(TicketSerializer(tickets,many=True).data)
        context['tickets_s']=tickets_s
        if request.user.has_perm(APP_NAME+".add_ticket"):
            context.update(AddTicketContext(request=request,project=project))
   
        remote_clients = project.all_remote_clients.all()
        context['remote_clients'] = remote_clients
        remote_clients_s = json.dumps(RemoteClientSerializer(remote_clients, many=True).data)
        context['remote_clients_s'] = remote_clients_s
        if request.user.has_perm(APP_NAME+".add_remoteclient"):
            context['operating_systems']=(i[0] for i in OperatingSystemNameEnum.choices)
            from accounting.repo import BrandRepo
            context['brands']=BrandRepo(request=request).list()
            context['add_remote_client_form'] = AddRemoteClientForm()
        return render(request,TEMPLATE_ROOT+"project.html",context)


class ProjectEditView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        # project.normalize()
        if project is None:
            title='پروژه وجود ندارد'
            body='پروژه وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context.update(ProjectContext(request=request,project=project))

        all_sub_ids=project.all_sub_ids(same_class=True,my_id=True)


        
        invoices=project.invoices.order_by('-event_datetime')
        invoices=project.all_invocie().order_by('-event_datetime')
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s




        
        invoice_lines=project.all_invocie_lines().order_by('row').order_by('invoice_id')
        invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s



        events=project.events.order_by('-event_datetime')
        events_s=json.dumps(EventSerializer(events,many=True).data)
        context['events']=events
        context['events_s']=events_s
        if request.user.has_perm('core.add_event'):
            context['add_event_to_project_form']=AddEventToProjectForm()


        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".add_invoice"):
            context.update(AddInvoiceContext(request=request))


            

        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".change_project"):
            context['add_invoice_to_project_form']=AddInvoiceToProjectForm()

        tickets=TicketRepo(request=request).list(project_id__in=all_sub_ids)
        context['tickets']=tickets
        tickets_s=json.dumps(TicketSerializer(tickets,many=True).data)
        context['tickets_s']=tickets_s
        if request.user.has_perm(APP_NAME+".add_ticket"):
            context.update(AddTicketContext(request=request,project=project))
   
        remote_clients = project.all_remote_clients.all()
        context['remote_clients'] = remote_clients
        remote_clients_s = json.dumps(RemoteClientSerializer(remote_clients, many=True).data)
        context['remote_clients_s'] = remote_clients_s
        if request.user.has_perm(APP_NAME+".add_remoteclient"):
            context['operating_systems']=(i[0] for i in OperatingSystemNameEnum.choices)
            from accounting.repo import BrandRepo
            context['brands']=BrandRepo(request=request).list()
            context['add_remote_client_form'] = AddRemoteClientForm()
        return render(request,TEMPLATE_ROOT+"project-edit.html",context)


class ProjectsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['WIDE_LAYOUT']=True
        projects = ProjectRepo(request=request).list(parent_id=None,*args, **kwargs)

        context['expand_projects']=True
        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s
        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form']=AddProjectForm
            organizations=OrganizationalUnitRepo(request=request).list()
            organizations_s=json.dumps(OrganizationalUnitSerializer(organizations,many=True).data)
            context['organizations_s']=organizations_s
        return render(request,TEMPLATE_ROOT+"projects.html",context)


class AllProjectsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['WIDE_LAYOUT']=True
        projects = ProjectRepo(request=request).list(*args, **kwargs)

        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s
        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form']=AddProjectForm
            organizations=OrganizationalUnitRepo(request=request).list()
            organizations_s=json.dumps(OrganizationalUnitSerializer(organizations,many=True).data)
            context['organizations_s']=organizations_s
        return render(request,TEMPLATE_ROOT+"projects.html",context)


class RemoteClientsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['WIDE_LAYOUT'] = True
        if context is None:
            return notPersmissionView(request=request)
        remote_clients = RemoteClientRepo(request=request).list()
        context['remote_clients'] = remote_clients
        remote_clients_s = json.dumps(RemoteClientSerializer(remote_clients, many=True).data)
        context['remote_clients_s'] = remote_clients_s
        context['expand_remote_clients']=True
        # if request.user.has_perm(APP_NAME+".add_material"):
            # context['add_material_form']=AddMaterialForm()
        return render(request, TEMPLATE_ROOT+"remote-clients.html", context)


class RemoteClientView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        
        remote_client = RemoteClientRepo(request=request).remote_client(*args, **kwargs)
        context['remote_client'] = remote_client
        return render(request, TEMPLATE_ROOT+"remote-client.html", context)


class TicketView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        ticket=TicketRepo(request=request).ticket(*args, **kwargs)
        if ticket is None:
            title='تیکت وجود ندارد'
            body='تیکت وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context.update(TicketContext(request=request,ticket=ticket))
 
        if request.user.has_perm(APP_NAME+".add_ticket"):
            context.update(AddTicketContext(request=request,project=ticket.project))
  
        return render(request,TEMPLATE_ROOT+"ticket.html",context)


class TicketsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        tickets = TicketRepo(request=request).list(parent_id=None,*args, **kwargs)

        context['tickets']=tickets
        tickets_s=json.dumps(TicketSerializer(tickets,many=True).data)
        context['tickets_s']=tickets_s
        if request.user.has_perm(APP_NAME+".add_ticket"):
            context.update(AddTicketContext(request=request,project=None))
            
        return render(request,TEMPLATE_ROOT+"tickets.html",context)

