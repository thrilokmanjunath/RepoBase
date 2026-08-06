from django import forms
from django.contrib.auth.models import User
from .models import Contact

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'attachment']

    def clean_message(self):
        msg = self.cleaned_data.get('message', '')
        if len(msg.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters")
        return msg
