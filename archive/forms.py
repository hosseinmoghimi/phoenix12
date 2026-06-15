from django import forms
class CreateFolderForm(forms.Form):
    name=forms.CharField( max_length=100, required=True)
    parent_id=forms.IntegerField(required=False)

class CreateFileForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
    folder_id=forms.IntegerField(required=True)

class OpenFolderForm(forms.Form):
    folder_id=forms.IntegerField(required=True)