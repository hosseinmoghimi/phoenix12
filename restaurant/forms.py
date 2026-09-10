from accounting.forms import forms

class AddFoodForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    code=forms.CharField(max_length=500,required=False)
    