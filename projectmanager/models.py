from django.db import models
from core.models import Event,FAILED,SUCCEED
from utility.models import DateHelper,DateTimeHelper,LinkHelper
from .enums import *
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
from .apps import APP_NAME
from accounting.models import InvoiceLine,Invoice
from django.core.files.storage import FileSystemStorage
from phoenix.server_settings import STATIC_URL,MEDIA_URL
from phoenix.server_settings import UPLOAD_ROOT,QRCODE_ROOT
IMAGE_FOLDER = APP_NAME+"/images/"
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')
from .enums import StatusColor


class Project(Event,LinkHelper,DateHelper):
    employer=models.ForeignKey("organization.organizationalunit", verbose_name=_("employer"),related_name="project_employed", on_delete=models.CASCADE)
    contractor=models.ForeignKey("organization.organizationalunit", verbose_name=_("contractor"),related_name="project_contracted", on_delete=models.CASCADE)
    type=models.CharField(_("تایپ"),max_length=50,choices=ProjectTypeEnum.choices,default=ProjectTypeEnum.TYPE_A)
    percentage_completed=models.IntegerField(_("درصد پیشرفت"),default=0)
    weight=models.IntegerField(_("وزن پروژه"),default=1)
    invoices=models.ManyToManyField("accounting.invoice", blank=True, verbose_name=_("invoices"))
    events=models.ManyToManyField("core.event",related_name="project_events", blank=True, verbose_name=_("events"))
    remote_clients=models.ManyToManyField("remoteclient", blank=True,verbose_name=_("remote_clients"))
    amount=models.IntegerField(_("ارزش پروژه"),default=0)
    @property
    def children(self):
        return Project.objects.filter(parent_id=self.id)
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    def normalize(self):
        sum=0
        for child in self.children.all():
            # child.normalize()
            sum+=child.amount
        for inv in self.invoices.filter(valid=True):
            sum+=inv.amount
            
        if not self.amount==sum:
            self.amount=sum
            super(Project,self).save()
            if self.parent_project is not None:
                self.parent_project.normalize()

    def save(self):
        (result,message,project)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="project"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Project,self).save()
        result=SUCCEED
        message="پروژه با موفقیت اضافه شد."
        return (result,message,project)
    @property
    def parent_project(self):
        if self.parent is None:
            return None
        return Project.objects.filter(pk=self.parent_id).first()
     
    
    @property    
    def total_price(self):
        return self.amount

    def all_invocie(self):
        ids=self.all_sub_ids(same_class=True,my_id=True)
        
        projects=Project.objects.filter(id__in=ids)
        invoice_ids=[]
        for proj in projects:
            for inv in proj.invoices.all():
                invoice_ids.append(inv.id) 
        return Invoice.objects.filter(id__in=invoice_ids)
    def all_sub_projects(self):
        ids=self.all_sub_ids(same_class=True,my_id=True)
        return Project.objects.filter(id__in=ids)
    def all_invocie_lines(self):
        ids=self.all_sub_ids(same_class=True,my_id=True)
         
        projects=Project.objects.filter(id__in=ids)
        invoice_ids=[]
        for proj in projects:
            for inv in proj.invoices.all():
                invoice_ids.append(inv.id)
        from accounting.models import InvoiceLine
        return InvoiceLine.objects.filter(invoice_id__in=invoice_ids)
  
    def get_status_color(self):
        return StatusColor(self)
    
    @property
    def all_remote_clients(self):
        ids=[]
        for remote_client in self.remote_clients.all():
            ids.append(remote_client.id)

            
        for project in Project.objects.filter(parent_id=self.id):
            for remote_client in project.all_remote_clients.all():
                ids.append(remote_client.id)
        aaa= RemoteClient.objects.filter(pk__in=ids)
        return aaa
    
     

class Ticket(models.Model,DateTimeHelper,LinkHelper):
    parent=models.ForeignKey("ticket",null=True,blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)
    title=models.CharField(_("title"),max_length=500)
    description=HTMLField(_("description"),max_length=5000,blank=True,null=True)
    person=models.ForeignKey("authentication.person",null=True,blank=True, verbose_name=_("شخص"), on_delete=models.PROTECT)
    project=models.ForeignKey("project",null=True,blank=True, verbose_name=_("پروژه"), on_delete=models.CASCADE)
    datetime_added=models.DateTimeField(_("date added"),auto_now=False,auto_now_add=True)
    type=models.CharField(_("تایپ"),max_length=50,choices=TicketTypeEnum.choices)
    status=models.CharField(_("وضعیت"),max_length=50,choices=TicketStatusEnum.choices,default=TicketStatusEnum.STARTED)
    file = models.FileField(_("فایل ضمیمه"), null=True, blank=True,upload_to=APP_NAME+'/ticket-files', storage=upload_storage, max_length=100)
    class_name="ticket"
    app_name=APP_NAME
    @property
    def thumbnail(self):
        return STATIC_URL+APP_NAME+f'/img/pages/thumbnail/ticket.png'
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return self.title
     
    def sub_tickets(self):
        return Ticket.objects.filter(parent_id=self.pk)
    def get_status_color(self):
        color="primary"
        if self.status==TicketStatusEnum.FINISHED:
            color="secondary"
        if self.status==TicketStatusEnum.IN_PROGRESS:
            color="info"
        if self.status==TicketStatusEnum.STARTED:
            color="danger" 
        return color
 
    def save(self,*args, **kwargs):
        result,message,ticket=FAILED,'',None
        super(Ticket,self).save()
        if self.id is not None and self.id>0:
            ticket=self
            result=SUCCEED
            message='تیکت با موفقیت ثبت شد.'
        return result,message,ticket

class RemoteClient(models.Model,LinkHelper):
   
    name=models.CharField(_("name"), max_length=100)
    active_directory=models.CharField(_("active_directory"),null=True,blank=True, max_length=100)
    work_group=models.CharField(_("work_group"),null=True,blank=True, max_length=50)
    os=models.CharField(_("Operating System (os)"),null=True,blank=True, max_length=50)
    url=models.CharField(_("url"),null=True,blank=True, max_length=500)
    local_ip=models.CharField(_("local_ip"),null=True,blank=True, max_length=50)
    remote_ip=models.CharField(_("remote_ip"),null=True,blank=True, max_length=50)
    any_desk_address=models.CharField(_("any_desk_address"),null=True,blank=True, max_length=50)
    any_desk_password=models.CharField(_("any_desk_password"),null=True,blank=True, max_length=50)
    dorsan_desk_address=models.CharField(_("dorsan_desk_address"),null=True,blank=True, max_length=50)
    dorsan_desk_password=models.CharField(_("dorsan_desk_password"),null=True,blank=True, max_length=50)
    brand=models.ForeignKey("accounting.brand",null=True,blank=True, verbose_name=_("brand"), on_delete=models.SET_NULL)
    product=models.ForeignKey("accounting.product",null=True,blank=True, verbose_name=_("product"), on_delete=models.SET_NULL)
    model_name=models.CharField(_("model name"),null=True,blank=True, max_length=50)
    id_name=models.CharField(_("id_name"),null=True,blank=True, max_length=50)
    mac_address=models.CharField(_("mac_address"),null=True,blank=True, max_length=50)
    serial_no=models.CharField(_("serial_no"),null=True,blank=True, max_length=50)
    pattern=models.CharField(_("pattern"),null=True,blank=True, max_length=50)
    part_no=models.CharField(_("part_no"),null=True,blank=True, max_length=50)
    username=models.CharField(_("username"),null=True,blank=True, max_length=50)
    password=models.CharField(_("password"),null=True,blank=True, max_length=50)
    identity=models.CharField(_("identity"),null=True,blank=True, max_length=50)
    wireless_mode=models.CharField(_("wireless_mode"),null=True,blank=True, max_length=50)
    wireless_band=models.CharField(_("wireless_band"),null=True,blank=True, max_length=50)
    ssid=models.CharField(_("ssid"),null=True,blank=True, max_length=50)
    preshared_key=models.CharField(_("preshared_key"),null=True,blank=True, max_length=50)
    frequency=models.CharField(_("frequency"),null=True,blank=True, max_length=50)
    protocol=models.CharField(_("protocol"),null=True,blank=True, max_length=50)
    channel_width=models.CharField(_("channel_width"),null=True,blank=True, max_length=50)
    adsl_username=models.CharField(_("adsl_username"),null=True,blank=True, max_length=50)
    adsl_password=models.CharField(_("adsl_password"),null=True,blank=True, max_length=50)
    telephone=models.CharField(_("telephone"),null=True,blank=True, max_length=50)
    contact=models.CharField(_("contact"),null=True,blank=True, max_length=50)
    description=models.TextField(_("description"),null=True,blank=True, max_length=2000)
    
    class_name="remoteclient"
    app_name=APP_NAME

    @property
    def get_project_absolute_url(self):
        project=self.project_set.first()
        if project is not None:
            return project.get_absolute_url()
   
    @property
    def get_project_title(self):
        project=self.project_set.first()
        if project is not None:
            return project.title
        
   
    class Meta:
        verbose_name = _("RemoteClient")
        verbose_name_plural = _("RemoteClients")

    def __str__(self):
        return self.name 

















