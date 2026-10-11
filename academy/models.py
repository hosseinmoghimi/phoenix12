from django.db import models
from core.models import LinkHelper,Page,reverse,STATIC_URL
from core.models import Event
from .enums import AttendanceStatusEnum
from django.utils.translation import gettext as _ 
from .apps import APP_NAME

class Course(models.Model,LinkHelper):

    title=models.CharField(_("title"), max_length=50)
    level=models.IntegerField(_("level"))
    code=models.CharField(_("code"), max_length=50)
    
    app_name=APP_NAME
    class_name="course"
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        from utility.constants import SUCCEED,FAILED
        super(Course,self).save()
        return SUCCEED,'واحد درسی با موفقیت ذخیره شد.',self


class Word(Page):
     

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")
 

    def save(self,*args, **kwargs):
        from utility.constants import SUCCEED,FAILED
        
        if self.class_name is None or self.class_name =='':
            self.class_name="word"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME

        super(Word,self).save()
        return SUCCEED,'کلمه با موفقیت ذخیره شد.',self
    

    def delete(self,*args, **kwargs):
        for word in Word.objects.filter(parent_id=self.id):
            word.parent_id=self.parent_id 
            super(Word,word).save() 
        super(Word,self).delete() 
    
    def get_breadcrumb_link(self):
            aaa=f"""
                        <li class="breadcrumb-item"><a href="{self.get_absolute_url()}">
                        <span class="farsi mx-2">
                        <img class="rounded" width="32" src="{self.thumbnail}">
                        {self.title}
                        </span>
                        </a></li> 
                        
                        
                        """
            if self.parent is None:
                return aaa
            return self.parent.get_breadcrumb_link()+aaa
        
    def get_breadcrumb(self):
            return f"""
            
                    <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{reverse('academy:word',kwargs={'pk':0})}">
                        <span class="farsi mx-2">
                        <img class="rounded" width="32" src="{STATIC_URL}{APP_NAME}/img/logo.png">
                        Home
                        </span>
                        </a></li> 

                        {self.get_breadcrumb_link()}
                    </ol>
                    </nav>
            """


class EducationalYear(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    class_name='educationalyear'
    app_name=APP_NAME
    class Meta:
        verbose_name = _("EducationalYear")
        verbose_name_plural = _("EducationalYears")

    def __str__(self):
        return self.name
    

class CourseClass(models.Model,LinkHelper):
    educational_year=models.ForeignKey("educationalyear", verbose_name=_("educational_year"), on_delete=models.CASCADE)
    course=models.ForeignKey("course", verbose_name=_("course"), on_delete=models.PROTECT)
    teachers=models.ManyToManyField("teacher",blank=True, verbose_name=_("teachers"))
    students=models.ManyToManyField("student",blank=True, verbose_name=_("students"))
    class_name="courseclass"
    app_name=APP_NAME
    
    @property
    def title(self):
        return str(self)

    class Meta:
        verbose_name = _("CourseClass")
        verbose_name_plural = _("CourseClasss")

    def __str__(self):
        return f'{self.educational_year} {self.course}' 


class Session(Event):
    course_class=models.ForeignKey("courseclass", verbose_name=_("courseclass"), on_delete=models.PROTECT)
    session_no=models.IntegerField(_("session_no"))
    class_room=models.CharField(_("class_room"), max_length=50)
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
    
    def save(self, *args, **kwargs):
         
        if not self.app_name:
            self.app_name = APP_NAME
        if not self.class_name:
            self.class_name = "session"
        return super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.course_class} جلسه {self.session_no}'

    
class Student(models.Model,LinkHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.PROTECT)
    
    class_name="student"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return f'{self.person}'
    
    def full_name(self):
        return self.person.full_name
 
class Teacher(models.Model,LinkHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.PROTECT)
    
    
    class_name="teacher"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return f'{self.person}'

    
    def full_name(self):
        return self.person.full_name


class Attendance(models.Model):
    session=models.ForeignKey("session", verbose_name=_("session"), on_delete=models.CASCADE)
    student=models.ForeignKey("student", verbose_name=_("student"), on_delete=models.CASCADE)
    teacher=models.ForeignKey("teacher", verbose_name=_("teacher"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    status=models.CharField(_("status"),choices=AttendanceStatusEnum.choices,default=AttendanceStatusEnum.PRESENT, max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def __str__(self):
        return f'{self.session} {self.student} {self.status} '
