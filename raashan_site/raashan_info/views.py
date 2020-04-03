from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from .models import *


class IndexView(TemplateView):
    template_name = 'raashan_info/index.html'

    def dispatch(self, request, *args, **kwargs):
        if (not request.user.get_worker()):
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
