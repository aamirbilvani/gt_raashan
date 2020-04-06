from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Worker

class CustomUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        username = cleaned_data.get('username')
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ('username', 'email')



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields



class RecipientForm(forms.Form):
    name = forms.CharField()
    cnic = forms.CharField(widget=forms.NumberInput)


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['user', 'organization']
