from resume.enums import ResumeItemEnum
from django import forms
from django.forms.fields import IntegerField

class EditResumeForm(forms.Form):
    resume_index_id=forms.IntegerField(required=True)

class AddContactMessageForm(forms.Form):
    resume_index_id=forms.IntegerField(required=True)
    subject=forms.CharField(max_length=200, required=True)
    email=forms.CharField(max_length=50, required=True)
    mobile=forms.CharField(max_length=13, required=False)
    message=forms.CharField(max_length=500, required=True)
    full_name=forms.CharField(max_length=50, required=True)
    app_name=forms.CharField(max_length=50, required=True)

class AddResumeItemForm(forms.Form):
    resume_index_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    priority=forms.IntegerField(required=False)

class AddResumeFactForm(AddResumeItemForm):
    count=forms.IntegerField(required=True)

class AddResumeSkillForm(AddResumeItemForm):
    percentage=forms.IntegerField(required=True)
    