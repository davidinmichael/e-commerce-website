from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "phone_number", "password"]

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data["email"]:
            raise forms.ValidationError("Email Address is required")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)