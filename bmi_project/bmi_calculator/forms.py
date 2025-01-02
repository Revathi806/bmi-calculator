from django import forms

class BMIForm(forms.Form):
    weight = forms.FloatField(label="Weight (kg)", min_value=0)#field will accept floating-point numbers
    height = forms.FloatField(label="Height (cm)", min_value=0)
class Login(forms.Form):
    uname=forms.CharField(label="Username")
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput)