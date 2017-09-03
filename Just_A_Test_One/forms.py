from django import forms

class Secure_Text_Class(forms.Form):

    secured_text = forms.CharField(max_length=10000)
