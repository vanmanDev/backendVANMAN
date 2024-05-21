from django.contrib import admin
from .models import Timesheets,ConfigSalary,leave_requests,Feedbacks

# Register your models here.
admin.site.register(Timesheets)
admin.site.register(ConfigSalary)
admin.site.register(leave_requests)
admin.site.register(Feedbacks)
