from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('workers', views.WorkerViewSet)
router.register('users', views.CustomUserViewSet)
router.register('organizations', views.OrganizationViewSet)
router.register('recipient', views.RecipientViewSet)
router.register('received', views.ReceivedViewSet)

urlpatterns = [
    path('', login_required(views.IndexView.as_view())),
    path('worker', login_required(views.WorkerView.as_view())),
    path('api/', include(router.urls))
]
