from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})



class Organization(models.Model):
    name = models.CharField('Organization Name', max_length=100)

    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    objects = CustomUserManager()

    def get_worker(self):
        if hasattr(self, 'worker'):
            return self.worker
        return None

    def __str__(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return self.username



class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=False)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)
    is_admin = models.BooleanField('Is Admin')

    def __str__(self):
        return str(self.user)



class Recipient(models.Model):
    name = models.CharField('Recipient Name', max_length=100)
    cnic = models.CharField('CNIC', db_index=True, max_length=13)

    def __str__(self):
        return self.name + ": {0}-{1}-{2}".format(self.cnic[0:5], self.cnic[5:12], self.cnic[12])



class Received(models.Model):
    date = models.DateTimeField('Date Received', auto_now_add=True)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{0} received raashan from {1} {2} of {3} on {4} at {5}".format(
            self.recipient,
            self.worker.user.first_name,
            self.worker.user.last_name,
            self.worker.organization,
            self.date.strftime('%Y-%m-%d'),
            self.date.strftime('%-I:%M %p'))
