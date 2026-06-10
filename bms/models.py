from django.db import models
from bms.apps import APP_NAME
from utility.enums import ColorEnum
from core.models import _,LinkHelper
from utility.calendar import PersianCalendar
from phoenix.settings import STATIC_URL,MEDIA_URL
IMAGE_FOLDER=APP_NAME+"/images/"

class Feeder(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    ip=models.CharField(_("ip"),default="192.168.45.200", max_length=20)
    serial_no=models.CharField(_("serial_no"), max_length=100)
    port=models.CharField(_("port"),default="80", max_length=5)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    pin=models.CharField(_("pin"),null=True,blank=True, max_length=50)
    is_protected=models.BooleanField(_("Is_protected"),default=False)
    thumbnail_origin=models.ImageField(_("thumbnail"), upload_to=IMAGE_FOLDER+"feeder/", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    
    def thumbnail(self):       
        if not self.thumbnail_origin:
            return STATIC_URL+APP_NAME+"/room.png"
        else:
            return MEDIA_URL+str(self.thumbnail_origin)

    app_name=APP_NAME
    class_name="feeder"
    @property
    def relays(self):
        return self.relay_set.all()
    class Meta:
        verbose_name = _("Feeder")
        verbose_name_plural = _("Feeders")

    def __str__(self):
        return self.name 


class Scenario(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    commands=models.ManyToManyField("command",blank=True, verbose_name=_("commands"))
    persons=models.ManyToManyField("authentication.person",blank=True, verbose_name=_("persons"))
    is_protected=models.BooleanField(_("is_protected"),default=False)
    pin=models.CharField(_("pin"),default="", max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    thumbnail_origin=models.ImageField(_("thumbnail"), upload_to=IMAGE_FOLDER+"scenario/", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    app_name=APP_NAME
    class_name="scenario"
 
    def thumbnail(self):       
        if not self.thumbnail_origin:
            return STATIC_URL+APP_NAME+"/room.png"
        else:
            return MEDIA_URL+str(self.thumbnail_origin)

    class Meta:
        verbose_name = _("Scenario")
        verbose_name_plural = _("Scenario")

    def __str__(self):
        return self.name 


class Relay(models.Model,LinkHelper):
    feeder=models.ForeignKey("feeder", verbose_name=_("feeder"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    enabled=models.BooleanField(_("enabled"), default=True)
    is_protected=models.BooleanField(_("is_protected"), default=False)
    register=models.CharField(_("register"), max_length=50)
    pin=models.CharField(_("pin"),null=True,blank=True,max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    state=models.BooleanField(_("state"),default=False)
    thumbnail_origin=models.ImageField(_("thumbnail"), upload_to=IMAGE_FOLDER+"relay/", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    priority=models.IntegerField(_("priority"),default=100)
    app_name=APP_NAME
    class_name="relay"
     
    def thumbnail(self):       
        if not self.thumbnail_origin:
            return STATIC_URL+APP_NAME+"/room.png"
        else:
            return MEDIA_URL+str(self.thumbnail_origin)
    @property
    def commands(self):
        return self.command_set.all()

    class Meta:
        verbose_name = _("Relay")
        verbose_name_plural = _("Relay")

    def __str__(self):
        return f"""{self.feeder} [{str(self.register)}] {self.name}"""
    


class Command(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    relay=models.ForeignKey("relay", verbose_name=_("relay"), on_delete=models.CASCADE)
    value=models.CharField(_("value"), max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    Iteration=models.IntegerField(_("Iteration"),default=1)
    for_home=models.BooleanField(_("for home"),default=False)
    persons=models.ManyToManyField("authentication.person",blank=True, verbose_name=_("person"))
    thumbnail_origin=models.ImageField(_("thumbnail"), upload_to=IMAGE_FOLDER+"command/", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    app_name=APP_NAME
    class_name="command"
    @property
    def ip(self):
        return self.relay.feeder.ip
    @property
    def port(self):
        return self.relay.feeder.port
    @property
    def pin(self):
        return self.relay.pin
    @property
    def register(self):
        return self.relay.register
    def thumbnail(self):       
        if not self.thumbnail_origin:
            return STATIC_URL+APP_NAME+"/room.png"
        else:
            return MEDIA_URL+str(self.thumbnail_origin)

    class Meta:
        verbose_name = _("Command")
        verbose_name_plural = _("Commands")

    def __str__(self):
        return self.name
 

class Log(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    person=models.ForeignKey("authentication.person",null=True,blank=True, verbose_name=_("person"), on_delete=models.CASCADE)
    relay=models.ForeignKey("relay", verbose_name=_("relay"), blank=True,null=True,on_delete=models.CASCADE)
    feeder=models.ForeignKey("feeder", verbose_name=_("feeder"), blank=True,null=True,on_delete=models.CASCADE)
    command=models.ForeignKey("command", verbose_name=_("command"), blank=True,null=True,on_delete=models.CASCADE)
    scenario=models.ForeignKey("scenario", verbose_name=_("scenario"), blank=True,null=True,on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    succeed=models.BooleanField(_("succeed"),default=True)
    app_name=APP_NAME
    class_name="log"
    def persian_date_added_tag(self):
        from utility.calendar import to_persian_datetime_tag
        return to_persian_datetime_tag(self.date_added)
    def persian_date_added(self):
        p=PersianCalendar().from_gregorian(self.date_added)
        e=self.date_added
        return f"""
            <span title="{e}">{p}</span>
        """
    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return self.title
 