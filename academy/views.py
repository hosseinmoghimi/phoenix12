from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL 
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,MessageView,PageContext
from .enums import *
from utility.calendar import PersianCalendar
import json

from .serializers import GroupSerializer,ScoreSerializer,ParentSerializer,CourseSerializer,WordSerializer,SchoolSerializer,MajorSerializer,CourseClassSerializer,AttendanceSerializer,TeacherSerializer,SessionSerializer,StudentSerializer,EducationalYearSerializer
from .repo import GroupRepo,CourseRepo,ScoreRepo,WordRepo,ParentRepo,CourseClassRepo,SchoolRepo,StudentRepo,MajorRepo,TeacherRepo,AttendanceRepo,SessionRepo,EducationalYearRepo
 
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='academy/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)


class SearchView(View):
    def post(self,request,*args, **kwargs):
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data['search_for']
            context=getContext(request=request)
           

            words=WordRepo(request=request).list(search_for=search_for).order_by('title')

            context['search_for']=search_for
            words_s=json.dumps(WordSerializer(words,many=True).data)
            context['words_s']=words_s
            context['words']=words
        
        return render(request,TEMPLATE_ROOT+"search.html",context)

 
class GetJsonBackupView(View):
    def get(self,request,*args, **kwargs):
        from django.http import JsonResponse
        origin_words=WordRepo(request=request).list()
        json_data={'words':[]}
        for word in origin_words:
            data={} 
            data['id']=word.id
            data['title']=word.title
            data['parent_id']=word.parent_id
            data['thumbnail_origin']=str(word.thumbnail_origin)
            json_data['words'].append(data)


        return JsonResponse(json_data,safe=False)
 

class CoursesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        courses =CourseRepo(request=request).list(*args, **kwargs)
        context['courses']=courses
        courses_s=json.dumps(CourseSerializer(courses,many=True).data)
        context['courses_s']=courses_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_course"):
            context['add_course_form']=AddCourseForm()
            from market.views import SupplierRepo
            suppliers=SupplierRepo(request=request).list()
            context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+"courses.html",context) 
 

class CourseView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 

        course =CourseRepo(request=request).course(*args, **kwargs) 
        context['course']=course
        course_s=json.dumps(CourseSerializer(course,many=False).data)
        context['course_s']=course_s

        course_classes=course.courseclass_set.all().order_by('level')
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s

  
 

        context[WIDE_LAYOUT]=True
        # context['NOT_NAVBAR']=True
        # context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"course.html",context) 
 

class SettingsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        courses =CourseRepo(request=request).list(*args, **kwargs)
        context['courses']=courses
        courses_s=json.dumps(CourseSerializer(courses,many=True).data)
        context['courses_s']=courses_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_course"):
            context['add_course_form']=AddCourseForm()
            from market.views import SupplierRepo
            suppliers=SupplierRepo(request=request).list()
            context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+"settings.html",context) 
 

class WordView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        word =WordRepo(request=request).word(*args, **kwargs) 
        if word is None:
            words=WordRepo(request=request).list(parent_id=None).order_by('title')
        else:
            context.update(PageContext(request=request,page=word))
            words=WordRepo(request=request).list(parent_id=word.id).order_by('title')
            context['word']=word
            word_s=json.dumps(WordSerializer(word,many=False).data)
            context['word_s']=word_s

        words_s=json.dumps(WordSerializer(words,many=True).data)
        context['words_s']=words_s
        context['words']=words
 
        if request.user.has_perm(APP_NAME+".add_word"):
            context['add_word_form']=AddWordForm()
        return render(request,TEMPLATE_ROOT+"word.html",context) 
 

class WordsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
         

        words=WordRepo(request=request).list().order_by('title')
        words_s=json.dumps(WordSerializer(words,many=True).data)
        context['words_s']=words_s
        context['words']=words
 
   
        return render(request,TEMPLATE_ROOT+"words.html",context) 
 
 
class TeacherView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        teacher =TeacherRepo(request=request).teacher(*args, **kwargs) 
        if teacher is None:
            mv=MessageView()
            mv.title='sdsd'
            mv.body='sdafdsgfdgffd'
            return mv.get(request=request)    
        context['teacher']=teacher
        teacher_s=json.dumps(TeacherSerializer(teacher,many=False).data)
        context['teacher_s']=teacher_s

        
        course_classes=teacher.courseclass_set.all().order_by('level').order_by('major__title')
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s
        context['course_classes']=course_classes

 
        return render(request,TEMPLATE_ROOT+"teacher.html",context) 


class TeachersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        teachers=TeacherRepo(request=request).list().order_by('person__last_name')
        teachers_s=json.dumps(TeacherSerializer(teachers,many=True).data)
        context['teachers_s']=teachers_s
        context['teachers']=teachers
        if request.user.has_perm(APP_NAME+".add_teacher"):
            context['add_teacher_form']=AddTeacherForm()
            
        return render(request,TEMPLATE_ROOT+"teachers.html",context) 



class TeachersExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        from utility.constants import FAILED,SUCCEED
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        teachers_excel_form=TeachersExcelForm(request.POST)
        if teachers_excel_form.is_valid():
            log=333
            cd=teachers_excel_form.cleaned_data
            if 'ids' in cd:
                ids=cd['ids']
                if ids is not None and not ids=="":
                    cd['ids']=json.loads(cd['ids'])
            teachers=TeacherRepo(request=request).list(**cd)
 
        now=PersianCalendar().date
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        for i,teacher in enumerate(teachers,start=1):
            line={
                'row':i,
                'id':teacher.id,
                'melli_code':teacher.person.melli_code,   
                'personneli_code':teacher.personneli_code,      
                'first_name':teacher.person.first_name,      
                'last_name':teacher.person.last_name,   
                'mobile':teacher.person.mobile,   
                'tel':teacher.person.tel,    
                'address':teacher.person.address,   
            }
            lines.append(line)
 
        headers=['ردیف',
                 'شناسه',
                 'کد ملی',
                 'کد پرسنلی',
                 'نام',
                 'نام خانوادگی',
                 'موبایل',
                 'تلفن',
                 'آدرس',
        ]
                
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'academy.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='teachers',
            title='teachers',
        )
        file_name=f"""Phoenix Academy Teachers {date.replace('/','').replace(':','')}.xlsx"""
        from django.http import HttpResponse
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response


class StudentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        student =StudentRepo(request=request).student(*args, **kwargs) 
        if student is None:
            mv=MessageView()
            return mv.get(request=request)

        
        groups=student.group_set.all()
        groups_s=json.dumps(GroupSerializer(groups,many=True).data)
        context['groups_s']=groups_s
        context['groups']=groups


        context['student']=student
        student_s=json.dumps(StudentSerializer(student,many=False).data)
        context['student_s']=student_s

        course_classes=student.courseclass_set.all().order_by('level')
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s
        context['course_classes']=course_classes


        scores=ScoreRepo(request=request).list(student_id=student.id).order_by('student__person__last_name')
        scores_s=json.dumps(ScoreSerializer(scores,many=True).data)
        context['scores_s']=scores_s
        context['scores']=scores 

        attendances=AttendanceRepo(request=request).list(student_id=student.id)
        context['attendances']=attendances
        attendances_s=json.dumps(AttendanceSerializer(attendances,many=True).data)
        context['attendances_s']=attendances_s


        if request.user.has_perm(APP_NAME+".add_student"):
            context['add_student_form']=AddStudentForm()
        return render(request,TEMPLATE_ROOT+"student.html",context) 


class AddStudentToGroupView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        students=StudentRepo(request=request).list().order_by('person__last_name')
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context['students_s']=students_s
        context['students']=students

        
        groups=GroupRepo(request=request).list().order_by('title')
        groups_s=json.dumps(GroupSerializer(groups,many=True).data)
        context['groups_s']=groups_s
        context['groups']=groups

        if request.user.has_perm(APP_NAME+".add_student"):
            context['add_student_to_group_form']=AddStudentToGroupForm()
    
        return render(request,TEMPLATE_ROOT+"add-student-to-group.html",context) 
    def post(self,request,*args, **kwargs):
        from .apis import AddStudentToGroupApi
        return AddStudentToGroupApi().post(request=request)

 
class StudentsExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        from utility.constants import FAILED,SUCCEED
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        students_excel_form=StudentsExcelForm(request.POST)
        if students_excel_form.is_valid():
            log=333
            cd=students_excel_form.cleaned_data
            if 'ids' in cd:
                ids=cd['ids']
                if ids is not None and not ids=="":
                    cd['ids']=json.loads(cd['ids'])
            students=StudentRepo(request=request).list(**cd)
 
        now=PersianCalendar().date
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        for i,student in enumerate(students,start=1):
            line={
                'row':i,
                'id':student.id,
                'melli_code':student.person.melli_code,   
                'first_name':student.person.first_name,      
                'last_name':student.person.last_name,   
                'father_name':student.parent.person.first_name if student.parent is not None else "",    
                'mobile':student.person.mobile,   
                'tel':student.person.tel,    
                'address':student.person.address,   
            }
            lines.append(line)
 
        headers=['ردیف',
                 'شناسه',
                 'کد ملی',
                 'نام',
                 'نام خانوادگی',
                 'نام پدر', 
                 'موبایل',
                 'تلفن',
                 'آدرس',
        ]
                
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'academy.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='students',
            title='students',
        )
        file_name=f"""Phoenix Academy Students {date.replace('/','').replace(':','')}.xlsx"""
        from django.http import HttpResponse
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

     
class AttendancesExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        from utility.constants import FAILED,SUCCEED
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        attendances_excel_form=AttendancesExcelForm(request.POST)
        if attendances_excel_form.is_valid():
            log=333
            cd=attendances_excel_form.cleaned_data
            if 'ids' in cd:
                ids=cd['ids']
                if ids is not None and not ids=="":
                    cd['ids']=json.loads(ids)
            attendances=AttendanceRepo(request=request).list(**cd)
 
        now=PersianCalendar().date
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        for i,attendance in enumerate(attendances,start=1):
            line={
                'row':i,
                'id':attendance.id,
                'school':attendance.session.course_class.school.name,   
                'course':attendance.session.course_class.course.title,   
                'session_no':attendance.session.session_no,   
                'date_time':attendance.session.persian_start_datetime(),   
                'class_room':attendance.session.class_room,   
                'teacher':attendance.session.course_class.teachers.first().person.full_name if attendance.session.course_class.teachers.first() is not None else "",   
                'first_name':attendance.student.person.first_name,      
                'last_name':attendance.student.person.last_name,   
                'status':attendance.status,   
                'father_name':attendance.student.parent.person.first_name if attendance.student.parent is not None else "",    
                # 'course_class':attendance.session.course_class.title,   
                # 'date_added':attendance.persian_date_added(),   
                'melli_code':attendance.student.person.melli_code,   
                'mobile':attendance.student.person.mobile,   
                'tel':attendance.student.person.tel,    
                'address':attendance.student.person.address,   
            }
            lines.append(line)
 
        headers=['ردیف',
                 'شناسه',
                 'آموزشگاه',
                 'واحد درسی',
                 'شماره جلسه',
                 'تاریخ جلسه',
                 'اتاق',
                 'دبیر',
                 'نام',
                 'نام خانوادگی',
                 'وضعیت',
                 'نام پدر', 
                #  'درس ارائه شده',
                #  'تاریخ ایجاد',
                 'کد ملی',
                 'موبایل',
                 'تلفن',
                 'آدرس',
        ]
                
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'academy.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='attendances',
            title='attendances',
        )
        file_name=f"""Phoenix Academy Attendances {date.replace('/','').replace(':','')}.xlsx"""
        from django.http import HttpResponse
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

     
class StudentsView(View):

    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        students=StudentRepo(request=request).list().order_by('person__last_name')
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context['students_s']=students_s
        context['students']=students
        if request.user.has_perm(APP_NAME+".add_student"):
            context['add_student_form']=AddStudentForm()
    
        return render(request,TEMPLATE_ROOT+"students.html",context) 


class MajorView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        major =MajorRepo(request=request).major(*args, **kwargs) 
        if major is None:
            mv=MessageView()
            return mv.get(request=request)

        
        context['major']=major
        major_s=json.dumps(MajorSerializer(major,many=False).data)
        context['major_s']=major_s

        course_classes=major.courseclass_set.all().order_by('level')
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s
        context['course_classes']=course_classes


 
 
        return render(request,TEMPLATE_ROOT+"major.html",context) 


class MajorsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        majors=MajorRepo(request=request).list().order_by('title')
        majors_s=json.dumps(MajorSerializer(majors,many=True).data)
        context['majors_s']=majors_s
        context['majors']=majors
        if request.user.has_perm(APP_NAME+".add_major"):
            context['add_major_form']=AddMajorForm()
    
        return render(request,TEMPLATE_ROOT+"majors.html",context) 


class CourseClassesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        course_classes =CourseClassRepo(request=request).list(*args, **kwargs)
        context['course_classes']=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_courseclass"):
            context['add_course_class_form']=AddCourseClassForm()
            courses=CourseRepo(request=request).list().order_by('title')
            context['courses']=courses
            educational_years=EducationalYearRepo(request=request).list()
            context['educational_years']=educational_years
            majors=MajorRepo(request=request).list()
            context['majors']=majors
            groups=GroupRepo(request=request).list()
            context['groups']=groups
            schools=SchoolRepo(request=request).list()
            context['schools']=schools
        return render(request,TEMPLATE_ROOT+"course-classes.html",context) 
 

class CourseClassView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        course_class =CourseClassRepo(request=request).course_class(*args, **kwargs) 
        context['course_class']=course_class
        course_class_s=json.dumps(CourseClassSerializer(course_class,many=False).data)
        context['course_class_s']=course_class_s

        teachers=course_class.teachers.all()
        teachers_s=json.dumps(TeacherSerializer(teachers,many=True).data)
        context['teachers_s']=teachers_s

        
        students=course_class.students.all().order_by('person__first_name').order_by('person__last_name')
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context['students_s']=students_s
        
        sessions=course_class.session_set.all().order_by('session_no')
        sessions_s=json.dumps(SessionSerializer(sessions,many=True).data)
        context['sessions_s']=sessions_s




        scores=ScoreRepo(request=request).list(course_class_id=course_class.id).order_by('student__person__last_name')
        scores_s=json.dumps(ScoreSerializer(scores,many=True).data)
        context['scores_s']=scores_s
        context['scores']=scores 

        context[WIDE_LAYOUT]=True
        # context['NOT_NAVBAR']=True
        # context['NOT_FOOTER']=True

        
        if request.user.has_perm(APP_NAME+".add_session"):
            context['add_session_form']=AddSessionForm()

            
        return render(request,TEMPLATE_ROOT+"course-class.html",context) 
 

class EducationalYearsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        educational_years =EducationalYearRepo(request=request).list(*args, **kwargs)
        context['educational_years']=educational_years
        educational_years_s=json.dumps(EducationalYearSerializer(educational_years,many=True).data)
        context['educational_years_s']=educational_years_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_educationalyear"):
            context['add_educational_year_form']=AddEducationalYearForm()
        return render(request,TEMPLATE_ROOT+"educational-years.html",context) 
 

class EducationalYearView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        from market.views import CustomerRepo,CartItemRepo,ShopSerializer
        educational_year =EducationalYearRepo(request=request).educational_year(*args, **kwargs) 
        context['educational_year']=educational_year
        educational_year_s=json.dumps(EducationalYearSerializer(educational_year,many=False).data)
        context['educational_year_s']=educational_year_s
 
        course_classes =educational_year.courseclass_set.all().order_by('level').order_by('major__title')
        context['course_classes']=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s

        context[WIDE_LAYOUT]=True
        # context['NOT_NAVBAR']=True
        # context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"educational-year.html",context) 
 

class SessionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        session =SessionRepo(request=request).session(*args, **kwargs) 
        if session is None:
            mv=MessageView()
            return mv.get(request=request)

        context[WIDE_LAYOUT]=True

        context.update(PageContext(request=request,page=session))
        context['session']=session
        session_s=json.dumps(SessionSerializer(session,many=False).data)
        context['session_s']=session_s
 
        
        attendances=AttendanceRepo(request=request).list(session_id=session.id).order_by('student__person__first_name').order_by('student__person__last_name')
        context['attendances']=attendances
        attendances_s=json.dumps(AttendanceSerializer(attendances,many=True).data)
        context['attendances_s']=attendances_s


        teachers=session.course_class.teachers.all()
        teachers_s=json.dumps(TeacherSerializer(teachers,many=True).data)
        context['teachers_s']=teachers_s

        
        students=session.course_class.students.all().order_by('person__first_name').order_by('person__last_name')
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context['students_s']=students_s


        if request.user.has_perm(APP_NAME+".add_attendance"):
            context['add_attendance_form']=AddAttendanceForm()
            

        return render(request,TEMPLATE_ROOT+"session.html",context) 


class SessionsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        sessions=SessionRepo(request=request).list().order_by('start_datetime')
        sessions_s=json.dumps(SessionSerializer(sessions,many=True).data)
        context['sessions_s']=sessions_s
        context['sessions']=sessions
        if request.user.has_perm(APP_NAME+".add_session"):
            context['add_session_form']=AddSessionForm()
    
        return render(request,TEMPLATE_ROOT+"sessions.html",context) 

 
class ScoresExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        from utility.constants import FAILED,SUCCEED
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        scores_excel_form=ScoresExcelForm(request.POST)
        if scores_excel_form.is_valid():
            log=333
            cd=scores_excel_form.cleaned_data
            if 'ids' in cd:
                ids=cd['ids']
                if ids is not None and not ids=="":
                    cd['ids']=json.loads(cd['ids'])
            scores=ScoreRepo(request=request).list(**cd)
 
        now=PersianCalendar().date
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        for i,score in enumerate(scores,start=1):
            line={
                'row':i,
                'id':score.id,
                'melli_code':score.student.person.melli_code,   
                'first_name':score.student.person.first_name,      
                'last_name':score.student.person.last_name,   
                'father_name':score.student.parent.person.first_name if score.student.parent is not None else "",    
                'course':score.course_class.course.title,   
                'educational_year':score.course_class.educational_year.name,    
                'school':score.course_class.school.name,    
                'type':score.score_type,    
                'score':score.score,   
            }
            lines.append(line)
 
        headers=['ردیف',
                 'شناسه',
                 'کد ملی',
                 'نام',
                 'نام خانوادگی',
                 'نام پدر', 
                 'واحد درسی',
                 'سال تحصیلی',
                 'آموزشگاه',
                 'نوع',
                 'نمره',
        ]
                
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'academy.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='scores',
            title='scores',
        )
        file_name=f"""Phoenix Academy Scores {date.replace('/','').replace(':','')}.xlsx"""
        from django.http import HttpResponse
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

    
class ScoresView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        context['expand_scores']=True
        scores=ScoreRepo(request=request).list().order_by('student__person__last_name')
        scores_s=json.dumps(ScoreSerializer(scores,many=True).data)
        context['scores_s']=scores_s
        context['scores']=scores 
    
        return render(request,TEMPLATE_ROOT+"scores.html",context) 


class NewScoreView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 

        student=StudentRepo(request=request).student(**kwargs)
        if student is None:
            mv=MessageView()
            return mv.get(request=request)
        context['student']=student

        context['expand_scores']=True
        scores=ScoreRepo(request=request).list().order_by('student__person__last_name')
        scores_s=json.dumps(ScoreSerializer(scores,many=True).data)
        context['scores_s']=scores_s
        context['scores']=scores 
        context['score_types']=(i[0] for i in ScoreTypeEnum.choices)
 
        course_classes=student.courseclass_set.all().order_by('level')
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s
        context['course_classes']=course_classes



        scores=[]
        scores_s=json.dumps(ScoreSerializer(scores,many=True).data)
        context['scores_s']=scores_s
        context['scores']=scores 


        return render(request,TEMPLATE_ROOT+"new-score.html",context) 


class SchoolView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        school =SchoolRepo(request=request).school(*args, **kwargs) 
        if school is None:
            mv=MessageView()
            return mv.get(request=request)

 
        context['school']=school
        school_s=json.dumps(SchoolSerializer(school,many=False).data)
        context['school_s']=school_s
 
        
        course_classes =school.courseclass_set.all().order_by('level').order_by('major__title')
        context['course_classes']=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s
         


        if request.user.has_perm(APP_NAME+".add_attendance"):
            context['add_attendance_form']=AddAttendanceForm()
            

        return render(request,TEMPLATE_ROOT+"school.html",context) 


class SchoolsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        schools=SchoolRepo(request=request).list().order_by('name')
        schools_s=json.dumps(SchoolSerializer(schools,many=True).data)
        context['schools_s']=schools_s
        context['schools']=schools
        if request.user.has_perm(APP_NAME+".add_school"):
            context['add_school_form']=AddSchoolForm()
    
        return render(request,TEMPLATE_ROOT+"schools.html",context) 


class ParentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        parent =ParentRepo(request=request).parent(*args, **kwargs) 
        if parent is None:
            mv=MessageView()
            return mv.get(request=request)

 
        context['parent']=parent
        parent_s=json.dumps(ParentSerializer(parent,many=False).data)
        context['parent_s']=parent_s
 
        students =parent.students.all()
        context['students']=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context['students_s']=students_s
         
        
        attendances=AttendanceRepo(request=request).list(student_id__in=(st.id for st in students)).order_by('-session__start_datetime')
        attendances=attendances
        context['attendances']=attendances
        attendances_s=json.dumps(AttendanceSerializer(attendances,many=True).data)
        context['attendances_s']=attendances_s

        

        if request.user.has_perm(APP_NAME+".add_student"):
            context['set_students_for_parent']=SetStudentsForParentForm()
            parents=ParentRepo(request=request).list()
            context['parents']=parents
            students=StudentRepo(request=request).list()
            context['students']=students
        if request.user.has_perm(APP_NAME+".add_attendance"):
            context['add_attendance_form']=AddAttendanceForm()
            

        return render(request,TEMPLATE_ROOT+"parent.html",context) 


class ParentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        parents=ParentRepo(request=request).list().order_by('person__last_name')
        parents_s=json.dumps(ParentSerializer(parents,many=True).data)
        context['parents_s']=parents_s
        context['parents']=parents
        if request.user.has_perm(APP_NAME+".add_parent"):
            context['add_parent_form']=AddParentForm()
    
        return render(request,TEMPLATE_ROOT+"parents.html",context) 


class GroupView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        group =GroupRepo(request=request).group(*args, **kwargs) 
        if group is None:
            mv=MessageView()
            return mv.get(request=request)

 
        context['group']=group
        group_s=json.dumps(GroupSerializer(group,many=False).data)
        context['group_s']=group_s
 


        
        course_classes =group.courseclass_set.all()
        context['course_classes']=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context['course_classes_s']=course_classes_s

        students =group.students.all().order_by('person__last_name') 
        context['students']=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context['students_s']=students_s
         


        if request.user.has_perm(APP_NAME+".add_attendance"):
            context['add_attendance_form']=AddAttendanceForm()
        if request.user.has_perm(APP_NAME+".add_student"):
            context['add_student_to_group_form']=AddStudentToGroupForm()

        return render(request,TEMPLATE_ROOT+"group.html",context) 


class GroupsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        

        groups=GroupRepo(request=request).list().order_by('title')
        groups_s=json.dumps(GroupSerializer(groups,many=True).data)
        context['groups_s']=groups_s
        context['groups']=groups
        if request.user.has_perm(APP_NAME+".add_group"):
            context['add_group_form']=AddGroupForm()
    
        return render(request,TEMPLATE_ROOT+"groups.html",context) 

