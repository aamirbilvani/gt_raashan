from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Organization, Recipient, Received, Worker


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm



class ReceivedInline(admin.StackedInline):
    model = Received
    extras = 3



class RecipientAdmin(admin.ModelAdmin):
    inlines = [ReceivedInline]



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Worker)
