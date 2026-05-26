from .models import Project,RemoteClient,Ticket
from .apps import APP_NAME
from core.repo import EventRepo
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *
 
 
class TicketRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Ticket.objects.filter(id=0)
        me_person=PersonRepo(request=request).me
        self.me_person=me_person
        if me_person is not None:
            if request.user.has_perm(APP_NAME+".view_ticket"):
                self.objects=Ticket.objects
                self.my_accounts=self.objects 
    
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            if parent_id is not None and parent_id>0:
                objects=objects.filter(parent_id=parent_id)  
        if "project_id" in kwargs:
            project_id=kwargs["project_id"]
            objects=objects.filter(project_id=project_id)  
        if "project_id__in" in kwargs:
            project_id__in=kwargs["project_id__in"]
            objects=objects.filter(project_id__in=project_id__in)  
        return objects.all()
        
    def ticket(self,*args, **kwargs):
        if "ticket_id" in kwargs and kwargs["ticket_id"] is not None:
            return self.objects.filter(pk=kwargs['ticket_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_ticket(self,*args,**kwargs):
        result,message,ticket=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_ticket"):
            message="دسترسی غیر مجاز"
            return result,message,ticket
        ticket=Ticket()
        if 'title' in kwargs:
            title=kwargs["title"]
            ticket.title=title

        if 'parent_id' in kwargs:
            parent_id=kwargs["parent_id"]
            if parent_id is not None and parent_id>0:
                ticket.parent_id=parent_id
        if 'project_id' in kwargs:
            ticket.project_id=kwargs["project_id"]
        if 'person_id' in kwargs:
            person_id=kwargs["person_id"] 
            if person_id is not None and person_id>0:
                ticket.person_id=person_id
            else:
                ticket.person_id=self.me_person.id
        if 'type' in kwargs:
            ticket.type=kwargs["type"]
        if 'description' in kwargs:
            ticket.description=kwargs["description"]
         
        if 'start_datetime' in kwargs:
            ticket.start_datetime=kwargs["start_datetime"]
            ticket.start_datetime=kwargs["start_datetime"]
            year=kwargs['start_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['start_datetime']=PersianCalendar().to_gregorian(kwargs["start_datetime"])
            ticket.start_datetime=kwargs['start_datetime']

 
        if 'end_datetime' in kwargs:
            ticket.end_datetime=kwargs["end_datetime"]
            ticket.end_datetime=kwargs["end_datetime"]
            year=kwargs['end_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['end_datetime']=PersianCalendar().to_gregorian(kwargs["end_datetime"])
            ticket.end_datetime=kwargs['end_datetime']

 
        if 'event_datetime' in kwargs:
            ticket.event_datetime=kwargs["event_datetime"]
            ticket.event_datetime=kwargs["event_datetime"]
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            ticket.event_datetime=kwargs['event_datetime']
             
        (result,message,ticket)=ticket.save()
        return result,message,ticket

  

class ProjectRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Project.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_project"):
                self.objects=Project.objects
                self.my_accounts=self.objects 
    
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(title__contains=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id) 
        if "organizational_unit_id" in kwargs:
            organizational_unit_id=kwargs["organizational_unit_id"]
            objects=objects.filter(Q(contractor_id=organizational_unit_id)  |Q(employer_id=organizational_unit_id))
        return objects.all()
        
    def project(self,*args, **kwargs):
        if "project_id" in kwargs and kwargs["project_id"] is not None:
            return self.objects.filter(pk=kwargs['project_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_project(self,*args,**kwargs):
        result,message,project=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_project"):
            message="دسترسی غیر مجاز"
            return result,message,project
        parent_id=None
        project=Project()
        if 'title' in kwargs:
            title=kwargs["title"]
        if 'parent_id' in kwargs:
            parent_id=kwargs["parent_id"]

        if len(Project.objects.filter(title=title).filter(parent_id=parent_id))>0:
            message='نام تکراری برای پروژه جدید'
            return FAILED,message,None
        project.title=title
        project.parent_id=parent_id
 
        if 'employer_id' in kwargs:
            project.employer_id=kwargs["employer_id"]
        if 'contractor_id' in kwargs:
            project.contractor_id=kwargs["contractor_id"]
        if 'type' in kwargs:
            project.type=kwargs["type"]
        if 'weight' in kwargs:
            project.weight=kwargs["weight"]
        if 'percentage_completed' in kwargs:
            project.percentage_completed=kwargs["percentage_completed"]
        if 'start_datetime' in kwargs:
            project.start_datetime=kwargs["start_datetime"]
            project.start_datetime=kwargs["start_datetime"]
            year=kwargs['start_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['start_datetime']=PersianCalendar().to_gregorian(kwargs["start_datetime"])
            project.start_datetime=kwargs['start_datetime']

 
        if 'end_datetime' in kwargs:
            project.end_datetime=kwargs["end_datetime"]
            project.end_datetime=kwargs["end_datetime"]
            year=kwargs['end_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['end_datetime']=PersianCalendar().to_gregorian(kwargs["end_datetime"])
            project.end_datetime=kwargs['end_datetime']

 
        if 'event_datetime' in kwargs:
            project.event_datetime=kwargs["event_datetime"]
            project.event_datetime=kwargs["event_datetime"]
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            project.event_datetime=kwargs['event_datetime']
            
        if project.parent is not None and project.contractor_id is None:
            project.contractor_id=project.parent_project.contractor_id

        if project.parent is not None and project.employer_id is None:
            project.employer_id=project.parent_project.employer_id
 
        
        (result,message,project)=project.save()
        return result,message,project

 
    def add_invoice(self,*args,**kwargs):
        result,message,invoice=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_invoice"):
            message="دسترسی غیر مجاز"
            return result,message,invoice
        from accounting.models import Invoice
        invoice=Invoice()
        if 'title' in kwargs:
            invoice.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                invoice.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            invoice.color=kwargs["color"]
        if 'code' in kwargs:
            invoice.code=kwargs["code"]
        if 'priority' in kwargs:
            invoice.priority=kwargs["priority"]
        if 'bedehkar_id' in kwargs:
            invoice.bedehkar_id=kwargs["bedehkar_id"]
        if 'bestankar_id' in kwargs:
            invoice.bestankar_id=kwargs["bestankar_id"]
        if 'event_datetime' in kwargs:
            
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            invoice.event_datetime=kwargs["event_datetime"]

        if 'type' in kwargs:
            invoice.type=kwargs["type"]

        project=self.project(id=kwargs['project_id']) 
        if invoice.parent_id is None:
            invoice.parent_id=kwargs['project_id']
        (result,message,invoice)=invoice.save()
        if project is not None:
            project.invoices.add(invoice.id)  
        return result,message,invoice



    def add_invoice_to_project(self,*args,**kwargs):
        result,message,invoice=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_invoice"):
            message="دسترسی غیر مجاز"
            return result,message,invoice
        from accounting.repo import InvoiceRepo
        invoice=InvoiceRepo(request=self.request).invoice(*args, **kwargs)
        project=self.project(*args, **kwargs)
        if project is None or invoice is None:
            message='داده های مرتبط یافت نشد.'
            return FAILED,message,None
        old=project.invoices.filter(pk=invoice.id).first()
        if old is not None:
            project.invoices.remove(invoice)
            project.save() 
            result=SUCCEED
            message='با موفقیت حذف شد.'
            return result,message,invoice


            
        project.invoices.add(invoice.id) 
        result=SUCCEED
        message='با موفقیت اضافه شد.'
        return result,message,invoice





    def normalize_project(self,*args, **kwargs):
        
        result=FAILED
        message="خطا در نرمال سازی "
        project=None
        if not self.request.user.has_perm(APP_NAME+".change_project"):
            message="عدم دسترسی مجاز "
            return result,message,project
        project=self.project(*args, **kwargs)
        if project is not None:
            project.normalize()
            result=SUCCEED
            message="با موفقیت نرمال سازی شد"
            return result,message,project

    

    def edit_project(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".change_project"):
            return None
        project=self.project(*args, **kwargs)
        if project is not None:
            if 'percentage_completed' in kwargs:
                project.percentage_completed=kwargs['percentage_completed']
            if 'start_datetime' in kwargs:
                project.start_datetime=kwargs['start_datetime']
            if 'end_datetime' in kwargs:
                project.end_datetime=kwargs['end_datetime']
            if 'status' in kwargs and kwargs['status'] is not None and not kwargs['status']=='':
                project.status=kwargs['status']
            if 'color' in kwargs and kwargs['color'] is not None and not kwargs['color']=='': 
                project.color=kwargs['color']
            if 'contractor_id' in kwargs:
                project.contractor_id=kwargs['contractor_id']
            if 'percentage_completed' in kwargs:
                project.percentage_completed=kwargs['percentage_completed']
            if 'weight' in kwargs:
                project.weight=kwargs['weight']
            if 'parent_id' in kwargs:
                parent_id=kwargs['parent_id']
                if parent_id<1:
                    project.parent=None
                elif parent_id>0 and len(Project.objects.filter(pk=parent_id))==1 and not parent_id==project.pk:
                    project.parent_id=parent_id
            if 'employer_id' in kwargs:
                project.employer_id=kwargs['employer_id']
            if 'title' in kwargs and kwargs['title'] is not None and not kwargs['title']=='':
                project.title=kwargs['title']
            if 'weight' in kwargs:
                project.weight=kwargs['weight']
                pass
            if 'priority' in kwargs:
                project.priority=kwargs['priority']
                pass
            if 'archive' in kwargs:
                project.archive=kwargs['archive']
            project.save()
            return project

    
    def add_event_to_project(self,*args, **kwargs):
        result,message,events=FAILED,'',[]
        if not self.request.user.has_perm(APP_NAME+".change_project"):
            message='دسترسی غیر مجاز'
            return FAILED,'',[]
        project=self.project(*args, **kwargs)
        if project is None:
            message='پروژه پیدا نشد.'
            return result,message,events

        event_id=kwargs['event_id']
        if event_id>0:
            event=EventRepo(request=self.request).event(*args, **kwargs)
        if event_id==0:

            result,message,event=EventRepo(request=self.request).add_event(*args, **kwargs)
        
        if event is None:
            message='رویداد پیدا نشد.'
            return result,message,events
        if event in project.events.all():
            project.events.remove(event.id)
            message='با موفقیت از پروژه حذف شد.'
            result=SUCCEED
        else:
            project.events.add(event.id)
            result=SUCCEED
            message='با موفقیت به پروژه اضافه شد.'
        return result,message,project.events.all()


class RemoteClientRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=RemoteClient.objects.all().order_by("-id")
        self.person=PersonRepo(*args, **kwargs).me
       

    def remote_client(self, *args, **kwargs):
        pk=0
        if 'remote_client_id' in kwargs:
            pk=kwargs['remote_client_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(name__contains=search_for)|Q(description__contains=search_for)|Q(local_ip__contains=search_for)|Q(remote_ip__contains=search_for))
           
        
        if 'product_id' in kwargs:
            product_id=kwargs['product_id']
            objects = objects.filter(product_id=product_id)
           

           
        
        if 'id__in' in kwargs:
            id__in=kwargs['id__in']
            objects = objects.filter(id__in=id__in)
           
         
           
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home'])) 
         

        return objects.all() 

    def add_remote_client(self,*args, **kwargs):
        result,message,remote_client=None,FAILED,""
        if not self.user.has_perm(APP_NAME+'.add_remoteclient'):
            message="شما مجوز لازم را برای افزودن سیستم کلاینت ندارید."
            return result,message,remote_client
        project_id=kwargs['project_id']
        project=Project.objects.filter(pk=project_id).first()
        if 'remote_client_id' in kwargs:
            remote_client_id=kwargs['remote_client_id']
            if remote_client_id is not None and remote_client_id >0:
                remote_client=self.remote_client(pk=remote_client_id)
                if remote_client is not None:
                    if project is not None:
                        if remote_client in project.remote_clients.all():
                            
                            project.remote_clients.remove(remote_client)
                            
                            result=SUCCEED
                            message="با موفقیت حذف شد."
                            remote_client=None

                        else:
                            project.remote_clients.add(remote_client)
                            
                            result=SUCCEED
                            message="با موفقیت اضافه شد."
                return result,message,remote_client
        kwargs.pop('remote_client_id')
        kwargs.pop('project_id')
        remote_client=RemoteClient(*args, **kwargs)
        if remote_client.brand_id==0 or remote_client.brand_id is None:
            remote_client.brand=None
        if remote_client.product_id==0 or remote_client.product_id is None:
            remote_client.product=None
        remote_client.save()
        if project is not None:
            project.remote_clients.add(remote_client)
            result=SUCCEED
            message="با موفقیت اضافه شد."
        else:
            message="پروژه مرتبط یافت نشد."

        return result,message,remote_client

 