from rest_framework import serializers
from .models import Worker, Organization, CustomUser, Recipient, Received

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']



class WorkerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Worker
        fields = ['id', 'organization', 'user', 'is_admin']
        depth = 1



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']



class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'name', 'cnic']



class ReceivedSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer()

    class Meta:
        model = Received
        fields = ['id', 'recipient', 'worker', 'date']
        depth = 2

