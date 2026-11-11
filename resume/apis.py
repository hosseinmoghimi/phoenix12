from .enums import ResumeItemEnum
from .models import ResumeFact, ResumeSkill
from rest_framework.views import APIView
from utility.constants import FAILED,SUCCEED
from .forms import AddContactMessageForm, AddResumeFactForm, AddResumeItemForm, AddResumeSkillForm
from .repo import ContactMessageRepo, ResumeFactRepo, ResumeIndexRepo, ResumeSkillRepo
from .serializers import ResumeFactSerializer, ResumeSkillSerializer
from django.http import JsonResponse


class BasicApi(APIView):
    def add_resume_item(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log=2
            add_resume_item_form=AddResumeItemForm(request.POST)
            if add_resume_item_form.is_valid():
                log=3
                resume_index_id=add_resume_item_form.cleaned_data['resume_index_id']
                language=add_resume_item_form.cleaned_data['language']
                item_type=add_resume_item_form.cleaned_data['item_type']
                title=add_resume_item_form.cleaned_data['title']
                if item_type==ResumeItemEnum.FACT:
                    add_resume_fact_form=AddResumeFactForm(request.POST)
                    if add_resume_fact_form.is_valid():
                        count=add_resume_fact_form.cleaned_data['count']
                        resume_fact=ResumeFactRepo(request=request,language=language).add(count=count,resume_index_id=resume_index_id,title=title)
                        return JsonResponse({'result':SUCCEED})
        context['log']=log
        return JsonResponse(context)
    def add_resume_fact(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_resume_fact_form=AddResumeFactForm(request.POST)
            if add_resume_fact_form.is_valid():
                log=3
                resume_index_id=add_resume_fact_form.cleaned_data['resume_index_id']
                title=add_resume_fact_form.cleaned_data['title']
                count=add_resume_fact_form.cleaned_data['count']
                priority=add_resume_fact_form.cleaned_data['priority']
                resume_fact=ResumeFactRepo(request=request,language=None).add(
                    count=count,
                    resume_index_id=resume_index_id,
                    title=title,
                    priority=priority
                    )
                if resume_fact is not None:
                    context['fact']=ResumeFactSerializer(resume_fact).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def add_resume_skill(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_resume_skill_form=AddResumeSkillForm(request.POST)
            if add_resume_skill_form.is_valid():
                log=3
                resume_index_id=add_resume_skill_form.cleaned_data['resume_index_id']
                title=add_resume_skill_form.cleaned_data['title']
                percentage=add_resume_skill_form.cleaned_data['percentage']
                priority=add_resume_skill_form.cleaned_data['priority']
                language=ResumeIndexRepo(request=request).resume_index(pk=resume_index_id).language
                
                resume_skill=ResumeSkillRepo(request=request,language=language).add(priority=priority,percentage=percentage,resume_index_id=resume_index_id,title=title)
                if resume_skill is not None:
                    context['result']=SUCCEED
                    context['skill']=ResumeSkillSerializer(resume_skill).data
        context['log']=log
        return JsonResponse(context)
    def add_contact_message(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_contact_message_form=AddContactMessageForm(request.POST)
            if add_contact_message_form.is_valid():
                resume_index_id=add_contact_message_form.cleaned_data['resume_index_id']
                full_name=add_contact_message_form.cleaned_data['full_name']
                email=add_contact_message_form.cleaned_data['email']
                mobile=add_contact_message_form.cleaned_data['mobile']
                subject=add_contact_message_form.cleaned_data['subject']
                message=add_contact_message_form.cleaned_data['message']
                app_name=add_contact_message_form.cleaned_data['app_name']
                contact_message=ContactMessageRepo(request=request,app_name=app_name).add(resume_index_id=resume_index_id,full_name=full_name,email=email,mobile=mobile,subject=subject,message=message)
                if contact_message is not None:
                    return JsonResponse({'result':SUCCEED})
        context['log']=log
        return JsonResponse(context)