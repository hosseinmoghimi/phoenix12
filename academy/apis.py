
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import ParentRepo,CourseRepo,EducationalYearRepo,WordRepo,GroupRepo,CourseClassRepo,MajorRepo,SessionRepo,SchoolRepo,TeacherRepo,StudentRepo,AttendanceRepo
from .serializers import ParentSerializer,EducationalYearSerializer,CourseSerializer,GroupSerializer,WordSerializer,SchoolSerializer,MajorSerializer,CourseClassSerializer,AttendanceSerializer,SessionSerializer,TeacherSerializer,StudentSerializer
from django.http import JsonResponse
from .forms import *
    
    
class AddCourseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_course_form=AddCourseForm(request.POST)
        if add_course_form.is_valid():
            log=333
            cd=add_course_form.cleaned_data
            result,message,course=CourseRepo(request=request).add_course(**cd)
            if course is not None:
                context['course']=CourseSerializer(course).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

    
class AddGroupApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_group_form=AddGroupForm(request.POST)
        if add_group_form.is_valid():
            log=333
            cd=add_group_form.cleaned_data
            result,message,group=GroupRepo(request=request).add_group(**cd)
            if group is not None:
                context['group']=GroupSerializer(group).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class ImportStudentsFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        import_students_form=ImportStudentFromExcelForm(request.POST,request.FILES)
        if import_students_form.is_valid():
            log=333
            cd=import_students_form.cleaned_data
            
            excel_file = request.FILES['file1']
            cd['excel_file']=excel_file
            result,message,students=StudentRepo(request=request).import_students_from_excel(**cd)
            if students is not None:
                context['students']=StudentSerializer(students,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddStudentToGroupApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_student_to_group_form=AddStudentToGroupForm(request.POST)
        if add_student_to_group_form.is_valid():
            log=333
            cd=add_student_to_group_form.cleaned_data
            result,message,group=GroupRepo(request=request).add_student_to_group(**cd)
            if group is not None:
                context['group']=GroupSerializer(group).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class ImportTeachersFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        import_teachers_form=ImportTeacherFromExcelForm(request.POST,request.FILES)
        if import_teachers_form.is_valid():
            log=333
            cd=import_teachers_form.cleaned_data
            
            excel_file = request.FILES['file1']
            cd['excel_file']=excel_file
            result,message,teachers=TeacherRepo(request=request).import_teachers_from_excel(**cd)
            if teachers is not None:
                context['teachers']=TeacherSerializer(teachers,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddStudentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_student_form=AddStudentForm(request.POST)
        if add_student_form.is_valid():
            log=333
            cd=add_student_form.cleaned_data
            result,message,student=StudentRepo(request=request).add_student(**cd)
            if result==SUCCEED:
                context['student']=StudentSerializer(student).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddEducationalYearApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_educational_year_form=AddEducationalYearForm(request.POST)
        if add_educational_year_form.is_valid():
            log=333
            cd=add_educational_year_form.cleaned_data
            result,message,educational_year=EducationalYearRepo(request=request).add_educational_year(**cd)
            if result==SUCCEED:
                context['educational_year']=EducationalYearSerializer(educational_year).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddMajorApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_major_form=AddMajorForm(request.POST)
        if add_major_form.is_valid():
            log=333
            cd=add_major_form.cleaned_data
            result,message,major=MajorRepo(request=request).add_major(**cd)
            if major is not None:
                context['major']=MajorSerializer(major).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

 
class AddAttendanceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_attendance_form=AddAttendanceForm(request.POST)
        if add_attendance_form.is_valid():
            log=333
            cd=add_attendance_form.cleaned_data
            result,message,attendance,attendances=AttendanceRepo(request=request).add_attendance(**cd)
            if attendance is not None:
                context['attendance']=AttendanceSerializer(attendance).data
                context['attendances']=AttendanceSerializer(attendances,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

 
class AddSchoolApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_school_form=AddSchoolForm(request.POST)
        if add_school_form.is_valid():
            log=333
            cd=add_school_form.cleaned_data
            result,message,school=SchoolRepo(request=request).add_school(**cd)
            if school is not None:
                context['school']=SchoolSerializer(school).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddTeacherApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_teacher_form=AddTeacherForm(request.POST)
        if add_teacher_form.is_valid():
            log=333
            cd=add_teacher_form.cleaned_data
            result,message,teacher=TeacherRepo(request=request).add_teacher(**cd)
            if teacher is not None:
                context['teacher']=TeacherSerializer(teacher).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
    
class AddParentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_parent_form=AddParentForm(request.POST)
        if add_parent_form.is_valid():
            log=333
            cd=add_parent_form.cleaned_data
            result,message,parent=ParentRepo(request=request).add_parent(**cd)
            if parent is not None:
                context['parent']=ParentSerializer(parent).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class SetStudentsForParentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        set_syudents_for_parent_form=SetStudentsForParentForm(request.POST)
        if set_syudents_for_parent_form.is_valid():
            log=333
            cd=set_syudents_for_parent_form.cleaned_data
            cd['students_ids']=json.loads(cd['students_ids'])
            result,message,students=ParentRepo(request=request).set_students_for_parent(**cd)
            if students is not None:
                context['students']=StudentSerializer(students,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    
 
class AddSessionApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_session_form=AddSessionForm(request.POST)
        if add_session_form.is_valid():
            log=333
            cd=add_session_form.cleaned_data
             
            result,message,session=SessionRepo(request=request).add_session(**cd)
            if session is not None:
                context['session']=SessionSerializer(session).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
   
class AddCourseClassApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_course_form=AddCourseClassForm(request.POST)
        if add_course_form.is_valid():
            log=333
            cd=add_course_form.cleaned_data
            result,message,course_class=CourseClassRepo(request=request).add_course_class(**cd)
            if course_class is not None:
                context['course_class']=CourseClassSerializer(course_class).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

  
class ImportFromJsonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
       
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            import_from_excel_form=ImportFromJsonForm(request.POST,request.FILES)
            if import_from_excel_form.is_valid():
                log=333
                
                json_file = request.FILES['file1']
                cd=import_from_excel_form.cleaned_data
                cd['json_file']=json_file
                result,message,words=WordRepo(request=request).import_from_json(**cd)
                if words is not None:
                    context['words']=WordSerializer(words,many=True).data
                  
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)        
    
    
class DeleteAllWordsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
       
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            delete_all_words_form=DeleteAllWordsForm(request.POST,request.FILES)
            if delete_all_words_form.is_valid():
                log=333
                
                cd=delete_all_words_form.cleaned_data
                result,message=WordRepo(request=request).delete_all_words(**cd) 
                  
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)        
    
    
class AddWordApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_word_form=AddWordForm(request.POST)
        if add_word_form.is_valid():
            log=333
            cd=add_word_form.cleaned_data
            result,message,word=WordRepo(request=request).add_word(**cd)
            if word is not None:
                context['word']=WordSerializer(word).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 