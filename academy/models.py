from utility.constants import SUCCEED,FAILED
from django.db import models
from core.models import LinkHelper,ImageHelper,Page,reverse,STATIC_URL
from core.models import Event
from .enums import AttendanceStatusEnum
from django.utils.translation import gettext as _ 
from .apps import APP_NAME
IMAGE_FOLDER = APP_NAME+"/images/"

class Course(models.Model,LinkHelper):

    title=models.CharField(_("title"), max_length=50) 
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'page/thumbnail/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    code=models.CharField(_("code"),null=True,blank=True, max_length=50)

    
    app_name=APP_NAME
    class_name="course"

    @property
    def thumbnail(self):
        from core.models import STATIC_URL,MEDIA_URL         
        thumbnail=""
        if self.thumbnail_origin is None or str(self.thumbnail_origin)=="":
            try:
                thumbnail= f"{STATIC_URL}{self.app_name}/img/course.jpg/"
            except:
                pass
        else:
            thumbnail= f"{MEDIA_URL}{self.thumbnail_origin}"

        return thumbnail

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        from utility.constants import SUCCEED,FAILED
        super(Course,self).save()
        return SUCCEED,'واحد درسی با موفقیت ذخیره شد.',self


    def class_count(self):
        return len(self.courseclass_set.all())


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
    major=models.ForeignKey("major", verbose_name=_("major"), on_delete=models.CASCADE)
    level=models.IntegerField(_("level"))
    school=models.ForeignKey("school", verbose_name=_("school"), on_delete=models.CASCADE)
    educational_year=models.ForeignKey("educationalyear", verbose_name=_("educational_year"), on_delete=models.CASCADE)
    course=models.ForeignKey("course", verbose_name=_("course"), on_delete=models.PROTECT)
    teachers=models.ManyToManyField("teacher",blank=True, verbose_name=_("teachers"))
    students=models.ManyToManyField("student",blank=True, verbose_name=_("students"))
    group=models.ForeignKey("group", verbose_name=_("group"),null=True,blank=True, on_delete=models.CASCADE)
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

    def save(self,*args, **kwargs):
        super(CourseClass,self).save()
        message="واحد ارائه شده ذخیره شد.."
        return SUCCEED,message,self

    def student_count(self):
        return len(self.students.all())

    
class Session(Event):
    course_class=models.ForeignKey("courseclass", verbose_name=_("courseclass"), on_delete=models.PROTECT)
    session_no=models.IntegerField(_("session_no"))
    class_room=models.CharField(_("class_room"),null=True,blank=True, max_length=50)
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
    
    def save(self, *args, **kwargs):
        if self.title is None or self.title=="":
            self.title=self.course_class.course.title +" جلسه "    +str(self.session_no)
        if not self.app_name:
            self.app_name = APP_NAME
        if not self.class_name:
            self.class_name = "session"
        super(Session, self).save(*args, **kwargs)
        message="جلسه ذخیره شد."
        return SUCCEED,message,self

    def __str__(self):
        return f'{self.course_class} جلسه {self.session_no}'
    @property
    def thumbnail(self):
        from core.models import STATIC_URL,MEDIA_URL         
        thumbnail=""
        if self.thumbnail_origin is None or str(self.thumbnail_origin)=="":
            return self.course_class.course.thumbnail
        else:
            thumbnail= f"{MEDIA_URL}{self.thumbnail_origin}"

        return thumbnail
    
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
    
    def first_name(self):
        return self.person.first_name
    
    def last_name(self):
        return self.person.last_name
    
    def melli_code(self):
        return self.person.melli_code
    
    def save(self,*args, **kwargs):
        super(Student,self).save()
        message="دانش آموز ذخیره شد.."
        return SUCCEED,message,self


    
class Parent(models.Model,LinkHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.PROTECT)
    students=models.ManyToManyField("student", verbose_name=_("students"))
    class_name="parent"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Parent")
        verbose_name_plural = _("Parents")

    def __str__(self):
        return f'{self.person}'
    
    def full_name(self):
        return self.person.full_name
    
    def first_name(self):
        return self.person.first_name
    
    def last_name(self):
        return self.person.last_name
    
    def melli_code(self):
        return self.person.melli_code
    
    def save(self,*args, **kwargs):
        super(Parent,self).save()
        message="ولی دانش آموز ذخیره شد."
        return SUCCEED,message,self


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

    def save(self,*args, **kwargs):
        super(Teacher,self).save()
        message="دبیر ذخیره شد."
        return SUCCEED,message,self

class Attendance(models.Model,LinkHelper):
    session=models.ForeignKey("session", verbose_name=_("session"), on_delete=models.CASCADE)
    student=models.ForeignKey("student", verbose_name=_("student"), on_delete=models.CASCADE)
    teacher=models.ForeignKey("teacher", verbose_name=_("teacher"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    status=models.CharField(_("status"),choices=AttendanceStatusEnum.choices,default=AttendanceStatusEnum.PRESENT, max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)
    class_name='attendance'
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def __str__(self):
        return f'{self.session} {self.student} {self.status} '

    def save(self,*args, **kwargs):
        super(Attendance,self).save()
        message="وضعیت حضور و غیاب ذخیره شد.."
        return SUCCEED,message,self


class Major(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    
    class_name='major'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Major")
        verbose_name_plural = _("Majors")

    def __str__(self):
        return self.title
 
    def save(self,*args, **kwargs):
        super(Major,self).save()
        message="رشته تحصیلی ذخیره شد.."
        return SUCCEED,message,self


class ActiveStudent(models.Model):
    student=models.ForeignKey("student", verbose_name=_("student"), on_delete=models.CASCADE)
    school=models.ForeignKey("school", verbose_name=_("school"), on_delete=models.CASCADE)
    major=models.ForeignKey("major", verbose_name=_("major"), on_delete=models.CASCADE)
    level=models.IntegerField(_("level"))

    class Meta:
        verbose_name = _("ActiveStudent")
        verbose_name_plural = _("ActiveStudents")

    def __str__(self):
        return f'{self.student}  {self.major}  {self.level}'

    def save(self,*args, **kwargs):
        super(ActiveStudent,self).save()
        message="دانش آموز ثبت نام شده ذخیره شد."
        return SUCCEED,message,self



class Group(models.Model,LinkHelper): 
    title=models.CharField(_("title"), max_length=50)
    code=models.CharField(_("code"),null=True,blank=True, max_length=50)
    students=models.ManyToManyField("student",blank=True, verbose_name=_("students"))
    
    class_name="group"
    app_name=APP_NAME
    def student_count(self):
        return len(self.students.all())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


    def save(self,*args, **kwargs):
        super(Group,self).save()
        message="گروه ذخیره شد."
        return SUCCEED,message,self


    
class School(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    code=models.CharField(_("code"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=500)

    class_name="school"  
    app_name=APP_NAME

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.name
 
    def save(self,*args, **kwargs):
        super(School,self).save()
        message="آموزشگاه ذخیره شد."
        return SUCCEED,message,self