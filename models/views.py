from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import api_view
from .models import Timesheets, ConfigSalary, leave_requests, Feedbacks
from .serializers import TimesheetsSerializer, ConfigSalarySerializer, leave_requestsSerializer, FeedbacksSerializer
from django.utils import timezone

class TimesheetList(generics.ListCreateAPIView):
    serializer_class = TimesheetsSerializer

    def get_queryset(self):
        queryset = Timesheets.objects.all()
        location = self.request.query_params.get('location')
        if location is not None:
            queryset = queryset.filter(testLocation=location)
        return queryset
    
    def delete(self, request, *args, **kwargs):
        try:
        # Delete all instances of Timesheets
            Timesheets.objects.all().delete()
            return Response({'message': 'All Timesheets deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TimesheetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TimesheetsSerializer
    queryset = Timesheets.objects.all()


class ConfigSalaryList(generics.ListCreateAPIView):
    serializer_class = ConfigSalarySerializer

    def get_queryset(self):
        queryset = ConfigSalary.objects.all()
        location = self.request.query_params.get('location')
        if location is not None:
            queryset = queryset.filter(testLocation=location)
        return queryset
    
class ConfigSalaryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConfigSalarySerializer
    queryset = ConfigSalary.objects.all()

class LeaveRequestList(generics.ListCreateAPIView):
    serializer_class = leave_requestsSerializer

    def get_queryset(self):
        queryset = leave_requests.objects.all()
        location = self.request.query_params.get('location')
        if location is not None:
            queryset = queryset.filter(testLocation=location)
        return queryset
    
    def delete(self, request, *args, **kwargs):
        try:
            # Delete all instances of leave_requests
            leave_requests.objects.all().delete()
            return Response({'message': 'All leave_requests deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LeaveRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = leave_requestsSerializer
    queryset = leave_requests.objects.all()

class FeedbackList(generics.ListCreateAPIView):
    serializer_class = FeedbacksSerializer

    def get_queryset(self):
        queryset = Feedbacks.objects.all()
        location = self.request.query_params.get('location')
        if location is not None:
            queryset = queryset.filter(testLocation=location)
        return queryset
    
    def delete(self, request, *args, **kwargs):
        try:
            # Delete all instances of Feedback
            Feedbacks.objects.all().delete()
            return Response({'message': 'All Feedbacks deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbacksSerializer
    queryset = Feedbacks.objects.all()
