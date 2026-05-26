from django import forms
from core.forms import SearchForm
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,required=True)
    password=forms.CharField(max_length=50,required=True)
    
class ChangePersonImageForm(forms.Form):
    person_id=forms.IntegerField(required=False)

  
class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50,required=True)
    password=forms.CharField(max_length=50,required=True)
    first_name=forms.CharField(max_length=50,required=True)
    last_name=forms.CharField(max_length=50,required=True)
    mobile=forms.CharField(max_length=50,required=True)

class SelectUserForm(forms.Form):
    user_id=forms.IntegerField(required=False)


class SelectPersonForm(forms.Form):
    person_id=forms.IntegerField(required=False)


class ChangePasswordForm(forms.Form):
    username=forms.CharField(max_length=100,required=True)
    old_password=forms.CharField(max_length=100,required=False)
    new_password=forms.CharField(max_length=100,required=True)
    
class AddPersonForm(forms.Form):
    user_id=forms.IntegerField(required=False)
    prefix=forms.CharField(max_length=11,required=False)
    gender=forms.CharField(max_length=11,required=False)
    title=forms.CharField(max_length=50,required=False)
    first_name=forms.CharField(max_length=50,required=False)
    last_name=forms.CharField(max_length=50,required=False)
    mobile=forms.CharField(max_length=50,required=False)
    email=forms.CharField(max_length=50,required=False)
    father_name=forms.CharField(max_length=50,required=False)
    bio=forms.CharField(max_length=2000,required=False)
    address=forms.CharField(max_length=200,required=False)
    type=forms.CharField(max_length=11,required=False)
    type2=forms.CharField(max_length=11,required=False)
    economic_no=forms.CharField(max_length=50,required=False)
    melli_code=forms.CharField(max_length=20,required=False)
    birth_date=forms.CharField(max_length=20,required=False)
    birth_location=forms.CharField(max_length=20,required=False)
    postal_code=forms.CharField(max_length=20,required=False)
    tel=forms.CharField(max_length=50,required=False)
 

class EditPersonForm(AddPersonForm):
    person_id=forms.IntegerField(required=True)



class ClearAllClipBoradItemForm(AddPersonForm):
    name=forms.CharField(max_length=100,required=False)



class   AddToClipBoradForm(forms.Form):
    name=forms.CharField(max_length=100,required=True)
    text=forms.CharField(max_length=100,required=True)
    
class DeleteMyLinkForm(forms.Form):
    my_link_id=forms.IntegerField(required=True)
    
class AddMyLinkForm(forms.Form):
    url=forms.CharField(max_length=5000,required=True)
    title=forms.CharField(max_length=5000,required=True)
    priority=forms.IntegerField(required=False)    
   