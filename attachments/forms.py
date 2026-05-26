from django import forms

class AddPagePrintForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    type=forms.CharField(max_length=50,required=False)


class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=True)
 
class AddPageCommentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    parent_id=forms.IntegerField(required=False)
    comment=forms.CharField(max_length=5000,required=True)
  
class DeletePageCommentForm(forms.Form):
    comment_id=forms.IntegerField(required=True)
 
class DeleteImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    image_id=forms.IntegerField(required=True)


class AddImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)

class AddLinkForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    url=forms.CharField(max_length=5000,required=True)
    title=forms.CharField(max_length=5000,required=True)
    priority=forms.IntegerField(required=False)
 
class AddDownloadForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=5000,required=True)
    priority=forms.IntegerField(required=False)


class AddLocationForm(forms.Form):
    title=forms.CharField(max_length=500,required=True)
    location=forms.CharField(max_length=500,required=True)
    page_id=forms.IntegerField(required=False)
          
class AddTagForm(forms.Form):
    title=forms.CharField(max_length=100,required=True)
    page_id=forms.IntegerField(required=False)
               
class AddPageLocationForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    location_id=forms.IntegerField(required=True)
class AddAreaForm(forms.Form):
    title=forms.CharField(max_length=500,required=True)
    code=forms.CharField(max_length=500,required=True)
    color=forms.CharField(max_length=500,required=True)
    area=forms.CharField(max_length=500,required=True)
               