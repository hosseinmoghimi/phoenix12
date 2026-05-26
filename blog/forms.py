from core.forms import forms

class AddBlogForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 