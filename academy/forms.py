from accounting.forms import forms
 

class AddCourseForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    code=forms.CharField(max_length=100, required=False)
    level=forms.IntegerField(required=True)
     
  
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=100, required=True)
     
  
class DeleteAllWordsForm(forms.Form):
    count=forms.IntegerField(required=False)

     
class AddCourseClassForm(forms.Form):
    course_id=forms.IntegerField(required=False)
    educational_year_id=forms.IntegerField(required=False)
     
     
class AddTeacherForm(forms.Form):
    count=forms.IntegerField(required=False)

     
class AddStudentForm(forms.Form):
    first_name=forms.CharField(max_length=100, required=True)
    last_name=forms.CharField(max_length=100, required=True)
    melli_code=forms.CharField(max_length=100, required=False)
    

class AddTeacherForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)
    

class AddWordForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)
    

class ImportFromJsonForm(forms.Form):
    count=forms.IntegerField(required=True)