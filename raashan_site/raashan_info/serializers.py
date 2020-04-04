from rest_framework import serializers
from .models import Worker, Organization, CustomUser, Recipient, Received

class WorkerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'organization', 'user', 'is_admin']



class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']



class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']



class RecipientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'name', 'cnic']



class ReceivedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Received
        fields = ['id', 'recipient', 'worker', 'date']
