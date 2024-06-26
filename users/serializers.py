from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'first_name', 'last_name', 'role', 'is_logged_in','supervisor','is_superuser']
