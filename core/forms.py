from django import forms 
class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=True)


class AddEventForm(forms.Form):
    title=forms.CharField(max_length=200, required=True)
    priority=forms.IntegerField(required=False)
    color=forms.CharField(max_length=50, required=False)
    status=forms.CharField(max_length=50, required=False)
    event_datetime=forms.CharField(max_length=50,required=False)
    start_datetime=forms.CharField(max_length=50,required=False)
    end_datetime=forms.CharField(max_length=50,required=False)
    description=forms.CharField(max_length=5000,required=False)


class EditPageForm(forms.Form):
    page_id=forms.IntegerField(required=False)
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=100, required=False)
    priority=forms.IntegerField(required=True)
    color=forms.CharField(max_length=50, required=False)
    status=forms.CharField(max_length=50, required=False)


class SetPageThumbnailHeaderForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    clear_thumbnail=forms.BooleanField(required=False)
    clear_header=forms.BooleanField(required=False)
    color=forms.CharField(max_length=50,required=False)
    title=forms.CharField(max_length=200,required=False)


class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50,required=False)
    app_name=forms.CharField(max_length=50,required=False)
    
class AddRelatedPageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    related_page_id=forms.IntegerField(required=True)
    bidirectional=forms.BooleanField(required=False)
    add_or_remove=forms.BooleanField(required=False)


class SetPagePriorityForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    priority=forms.IntegerField(required=True)