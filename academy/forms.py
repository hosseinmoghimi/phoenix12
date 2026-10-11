from accounting.forms import forms
 

class AddCourseForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    supplier_id=forms.IntegerField(required=True)
     
  
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=100, required=True)
     
  
class DeleteAllWordsForm(forms.Form):
    count=forms.IntegerField(required=False)

     
class AddCourseClassForm(forms.Form):
    count=forms.IntegerField(required=False)
     
     
class AddTeacherForm(forms.Form):
    count=forms.IntegerField(required=False)

     
class AddStudentForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)
    

class AddTeacherForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)
    

class AddWordForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)
    

class ImportFromJsonForm(forms.Form):
    count=forms.IntegerField(required=True)