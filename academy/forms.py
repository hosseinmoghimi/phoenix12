from accounting.forms import forms
 

class AddCourseForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    supplier_id=forms.IntegerField(required=True)
     
 