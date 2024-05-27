from django.urls import path,include
from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('reset_password/', include('django_rest_passwordreset.urls', namespace='reset_password')),
]
