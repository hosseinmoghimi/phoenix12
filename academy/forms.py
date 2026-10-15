from accounting.forms import forms
 

class AddCourseForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    code=forms.CharField(max_length=100, required=False)
    level=forms.IntegerField(required=True)

     
class AddMajorForm(forms.Form):
    title=forms.CharField(max_length=20, required=True)


class AddSessionForm(forms.Form):
    start_datetime=forms.CharField(max_length=20, required=True)
    end_datetime=forms.CharField(max_length=20, required=True)
    session_no=forms.IntegerField(required=True)
    course_class_id=forms.IntegerField(required=True)
    class_room=forms.CharField(max_length=50, required=False) 

  
class AddAttendanceForm(forms.Form):
    description=forms.CharField(max_length=100, required=False)
    status=forms.CharField(max_length=100, required=True)
    student_id=forms.IntegerField(required=True)
    session_id=forms.IntegerField(required=True)

     
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=100, required=True)
     
  
class DeleteAllWordsForm(forms.Form):
    count=forms.IntegerField(required=False)

class AddEducationalYearForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
     
class AddCourseClassForm(forms.Form):
    level=forms.IntegerField(required=True)
    course_id=forms.IntegerField(required=True)
    major_id=forms.IntegerField(required=True)
    school_id=forms.IntegerField(required=True)
    educational_year_id=forms.IntegerField(required=True)
     
     
class AddTeacherForm(forms.Form):
    count=forms.IntegerField(required=False)

     
class AddStudentForm(forms.Form):
    first_name=forms.CharField(max_length=100, required=True)
    last_name=forms.CharField(max_length=100, required=True)
    melli_code=forms.CharField(max_length=100, required=False)
    

class AddTeacherForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)


class AddSchoolForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)
    code=forms.CharField(max_length=100, required=False)
    tel=forms.CharField(max_length=100, required=False)
    address=forms.CharField(max_length=100, required=False)

  
class AddWordForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)
    

class ImportFromJsonForm(forms.Form):
    count=forms.IntegerField(required=True)