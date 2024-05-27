from django.urls import path
from . import views

urlpatterns = [
    path('timesheets/', views.TimesheetList.as_view()),
    path('timesheets/<int:pk>/', views.TimesheetDetail.as_view()),
    path('config_salary/', views.ConfigSalaryList.as_view()),
    path('config_salary/<int:pk>/', views.ConfigSalaryDetail.as_view()),
    path('leave_requests/', views.LeaveRequestList.as_view()),
    path('leave_requests/<int:pk>/', views.LeaveRequestDetail.as_view()),
    path('feedbacks/', views.FeedbackList.as_view()),
    path('feedbacks/<int:pk>/', views.FeedbackDetail.as_view()),
    path('attendance-summary/<int:user_id>/', views.AttendanceSummary.as_view(), name='attendance-summary'),
]

