from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from rest_framework.decorators import api_view
from .models import Timesheets, ConfigSalary, leave_requests, Feedbacks
from .serializers import TimesheetsSerializer, ConfigSalarySerializer, leave_requestsSerializer, FeedbacksSerializer
from django.utils import timezone
from users.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

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
    
    def perform_create(self, serializer):
        with transaction.atomic():
            try:
                leave_request = serializer.save()
                supervisor = leave_request.user.supervisor
                if supervisor and supervisor.email:
                    self.send_leave_request_email(leave_request, supervisor.email, "Leave Request")
            except Exception as e:
                logger.error(f"Error during leave request creation: {str(e)}")
                raise e

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        leave_request = serializer.instance
        supervisor = leave_request.user.supervisor
        if supervisor and supervisor.email:
            self.send_leave_request_email(leave_request, supervisor.email, "Updated Leave Request")
        
        return Response(serializer.data)

    def perform_patch(self, serializer):
        with transaction.atomic():
            try:
                serializer.save()
            except Exception as e:
                logger.error(f"Error during leave request update: {str(e)}")
                raise e

    def send_leave_request_email(self, leave_request, supervisor_email, subject):
        try:
            datetime_start_formatted = leave_request.datetime_start.strftime("Date: %d %B %Y Time: %I:%M:%S %p")
            datetime_end_formatted = leave_request.datetime_end.strftime("Date: %d %B %Y Time: %I:%M:%S %p")
            duration = (leave_request.datetime_end - leave_request.datetime_start)
            days = duration.days
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            first_name = leave_request.user.first_name
            last_name = leave_request.user.last_name

            email_html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{subject}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #333;
                    }}
                    p {{
                        color: #555;
                    }}
                    .details {{
                        margin-top: 20px;
                        padding-top: 10px;
                        border-top: 1px solid #ccc;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{subject}</h1>
                    <p>Intern <strong>{first_name} {last_name}</strong> has requested leave:</p>
                    <div class="details">
                        <p><strong>Requested Period:</strong> <strong>[ {datetime_start_formatted} ]</strong> to <strong>[ {datetime_end_formatted} ]</strong></p>
                        <p><strong>Duration:</strong> {days} days, {hours} hours, {minutes} minutes</p>
                        <p><strong>Type of Leave:</strong> {leave_request.get_type_of_leave_display()}</p>
                        <p><strong>Reason:</strong> {leave_request.description}</p>
                        <p><strong>Contact:</strong> {leave_request.tel}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            send_mail(
                f"{subject} from {first_name} {last_name}",
                "",
                "VANMAN System <your-email@example.com>",
                [supervisor_email],
                html_message=email_html_message,
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error sending leave request email: {str(e)}")
            raise e

    
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

class AttendanceSummary(APIView):

    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        timesheets = Timesheets.objects.filter(user=user)
        total_wages = 0

        for timesheet in timesheets:
            if timesheet.status == '2':
                if timesheet.type_of_work == 'Work From Home':
                    total_wages += 80
                elif timesheet.type_of_work == 'Work at Office':
                    total_wages += 150
            else:
                total_wages += 0

        total_days = timesheets.count()
        absent_days = timesheets.filter(status=0).count()
        wait_days = timesheets.filter(status=1).count()
        work_days = timesheets.filter(type_sign__in=['normal','backdate','holiday','backdate(holiday)'],status=2).count()

        data = {
            'total_days': total_days,
            'absent_days': absent_days,
            'work_days': work_days,
            'wait_days': wait_days,
            'absent_percentage': (absent_days / total_days) * 100 if total_days else 0,
            'work_percentage': (work_days / total_days) * 100 if total_days else 0,
            'wait_percentage': (wait_days / total_days) * 100 if total_days else 0,
            'total_wages_user': total_wages
        }
        return Response(data)
