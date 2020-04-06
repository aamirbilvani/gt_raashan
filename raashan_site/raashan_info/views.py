from django.views.generic import FormView, CreateView
from django.shortcuts import redirect
from rest_framework import viewsets
from datetime import datetime

from .models import *
from .serializers import *
from .forms import RecipientForm


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



class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all().order_by('id')
    serializer_class = WorkerSerializer



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer



class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer



class ReceivedViewSet(viewsets.ModelViewSet):
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



class RecipientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all().order_by('id')
    serializer_class = RecipientSerializer
