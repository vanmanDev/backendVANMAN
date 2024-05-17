from rest_framework import serializers
from .models import Timesheets, ConfigSalary, leave_requests, Feedbacks

class TimesheetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheets
        fields = ['id','date', 'time_in', 'time_out', 'description' , 'type_of_work', 'who_signed', 'user', 'type_sign', 'status']

class ConfigSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigSalary
        fields = ['id','WOF', 'WFH']

class leave_requestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = leave_requests
        fields = ['id','datetime_start', 'datetime_end', 'datetime_requested', 'description', 'status', 'who_signed', 'tel', 'type_of_leave', 'user']

class FeedbacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = ['id','datetime_send', 'title', 'type', 'description','status', 'user']
