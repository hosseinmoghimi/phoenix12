from django import forms
class SendSMSForm(forms.Form):
    message=forms.CharField( max_length=1000, required=True)
    receptor=forms.CharField( max_length=50000, required=True)
    

class SendMessageForm(forms.Form):
    message_title=forms.CharField( max_length=100, required=False)
    message_body=forms.CharField( max_length=100, required=True)
    channel_id=forms.IntegerField(required=True)
    event=forms.CharField( max_length=50, required=False)
    
class SendNotificationForm(forms.Form):
    message_title=forms.CharField( max_length=100, required=False)
    message_body=forms.CharField( max_length=100, required=True)
    member_id=forms.IntegerField(required=True)