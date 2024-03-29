from django.views.generic import FormView, CreateView
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from rest_framework import mixins
from datetime import datetime

from .models import *
from .serializers import *
from .forms import RecipientForm, CustomUserCreationForm


class IndexView(FormView):
    template_name = 'raashan_info/index.html'
    form_class = RecipientForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.get_worker():
            return redirect('/worker')
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # get the form data
        cnic = form.cleaned_data['cnic']
        name = form.cleaned_data['name']

        # get the worker and recipient objects from the DB
        worker = self.request.user.get_worker()
        recipient = Recipient.objects.filter(cnic=cnic).first()

        if recipient:
            # if recipient's name is different from the saved name, update it
            if recipient.name != name:
                recipient.name = name
                recipient.save()
        # if recipient doesn't exist, create it
        else:
            recipient = Recipient(name=name, cnic=cnic)
            recipient.save()

        # create the received object
        received = Received(recipient_id=recipient.id, worker_id=worker.id, date=datetime.now())
        received.save()

        return super().form_valid(form)



class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    # if form validation succeeds, create the user object, then login the user
    # Additionally, create a worker for the user.
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        organization = form.cleaned_data.get('organization')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        worker = Worker(user_id=user.id, organization_id=organization, is_admin=False)
        worker.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context['back_url'] = 'login'
        return context


class WorkerView(CreateView):
    model = Worker
    fields = '__all__'
    template_name = 'raashan_info/worker.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(WorkerView, self).get_context_data(**kwargs)
        current_user = self.request.user
        if current_user.first_name and current_user.last_name:
            context['readable_username'] = "{} {}".format(current_user.first_name, current_user.last_name)
        else:
            context['readable_username'] = current_user.username
        return context



class WorkerViewSet(ReadOnlyModelViewSet):
    queryset = Worker.objects.all().order_by('id')
    serializer_class = WorkerSerializer
    permission_classes = [IsAdminUser]



class CustomUserViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]



class OrganizationViewSet(GenericViewSet, 
                          mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer



class ReceivedViewSet(ReadOnlyModelViewSet):
    queryset = Received.objects.all().order_by('-date')
    serializer_class = ReceivedSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        cnic_param = self.request.query_params.get('cnic')

        recipient = Recipient.objects.filter(cnic=cnic_param).first()
        if recipient:
            qs = qs.filter(recipient_id=recipient.id)
        else:
            qs = Received.objects.none()

        return qs



class RecipientViewSet(ReadOnlyModelViewSet):
    queryset = Recipient.objects.all().order_by('id')
    serializer_class = RecipientSerializer
    permission_classes = [IsAdminUser]
