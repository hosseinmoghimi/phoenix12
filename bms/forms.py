 
from django import forms

class SetRelayForm(forms.Form):
    feeder_id=forms.IntegerField(required=True)
    register=forms.IntegerField(required=True)
    state=forms.BooleanField(required=False)

class SetRelayStateForm(forms.Form):
    relay_id=forms.IntegerField(required=True)
    state=forms.BooleanField(required=False)

class ExecuteCommandForm(forms.Form):
    command_id=forms.IntegerField(required=True)
    pin=forms.CharField(max_length=50, required=False)

class RunScenarionForm(forms.Form):
    scenario_id=forms.IntegerField(required=True)
    pin=forms.CharField(max_length=50, required=False)

class GetLogForm(forms.Form):
    page=forms.IntegerField(required=True)
    per_page=forms.IntegerField(required=False)
             