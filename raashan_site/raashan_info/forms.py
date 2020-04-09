from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Worker, Organization
from django.db.utils import OperationalError

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    # Get the organization values from the DB to populate into the select box
    try:
        organizations = Organization.objects.all()
        organization_choices = []
        for org in organizations:
            organization_choices.append((org.id, org.name))

        organization = forms.ChoiceField(
            required=False,
            choices=organization_choices,
        )
    except OperationalError:
        # this happens when DB doesn't yet exist
        pass


    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        username = cleaned_data.get('username')
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



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
