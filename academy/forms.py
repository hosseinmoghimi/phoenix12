from accounting.forms import forms
 

class AddCourseForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    code=forms.CharField(max_length=100, required=False)

     
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

  
class AddStudentToGroupForm(forms.Form):
    student_melli_code=forms.CharField(max_length=100, required=False)
    group_code=forms.CharField(max_length=100, required=False)
    student_id=forms.IntegerField(required=False)
    group_id=forms.IntegerField(required=False)


class ImportStudentFromExcelForm(forms.Form):
    count=forms.IntegerField( required=False)


class StudentsExcelForm(forms.Form):
    ids=forms.CharField( max_length=10000, required=False)


class ImportTeacherFromExcelForm(forms.Form):
    count=forms.IntegerField( required=False)


class TeachersExcelForm(forms.Form):
    ids=forms.CharField( max_length=10000, required=False)

      
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
    group_id=forms.IntegerField(required=False)
    educational_year_id=forms.IntegerField(required=True)
     
     
class AddParentForm(forms.Form):
    first_name=forms.CharField(max_length=100, required=False)
    last_name=forms.CharField(max_length=100, required=False)
    melli_code=forms.CharField(max_length=100, required=False)
    person_id=forms.IntegerField(required=False)


class SetStudentsForParentForm(forms.Form):
    parent_id=forms.IntegerField(required=True)
    students_ids=forms.CharField(max_length=500,required=True)
 

     
class AddStudentForm(forms.Form):
    first_name=forms.CharField(max_length=100, required=False)
    last_name=forms.CharField(max_length=100, required=False)
    melli_code=forms.CharField(max_length=100, required=False)
    person_id=forms.IntegerField(required=False)


class AddTeacherForm(forms.Form):
    first_name=forms.CharField(max_length=100, required=False)
    last_name=forms.CharField(max_length=100, required=False)
    melli_code=forms.CharField(max_length=100, required=False)
    person_id=forms.IntegerField(required=False)
    personneli_code=forms.CharField(max_length=12, required=False)

 
class AddSchoolForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)
    code=forms.CharField(max_length=100, required=False)
    tel=forms.CharField(max_length=100, required=False)
    address=forms.CharField(max_length=100, required=False)

  
class AddWordForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    parent_id=forms.IntegerField(required=True)


class AddGroupForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    code=forms.CharField(max_length=100, required=False)


class ImportFromJsonForm(forms.Form):
    count=forms.IntegerField(required=True)