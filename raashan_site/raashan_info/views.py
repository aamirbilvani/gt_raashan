from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from .models import *
from rest_framework import viewsets
from .serializers import *


class IndexView(TemplateView):
    template_name = 'raashan_info/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.get_worker():
            return redirect('/worker')
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['back_url'] = "/"
        return context



class WorkerView(CreateView):
    model = Worker
    fields = '__all__'
    template_name = 'raashan_info/worker.html'

    def get_success_url(self):
        return '/'



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
