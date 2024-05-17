# Generated by Django 5.0.3 on 2024-05-16 08:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WOF', models.FloatField()),
                ('WFH', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Feedbacks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_send', models.DateTimeField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=256)),
                ('status', models.CharField(choices=[(0, 'we have received your message'), (1, 'We are proceesing this'), (2, 'we aware of this or completed processing this')], default=0, max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='leave_requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField(max_length=50)),
                ('datetime_end', models.DateTimeField(max_length=50)),
                ('datetime_requested', models.DateTimeField(auto_now_add=True, max_length=50)),
                ('description', models.CharField(max_length=256)),
                ('status', models.CharField(choices=[(0, 'rejected'), (1, 'pending'), (2, 'approved')], default=1, max_length=50)),
                ('who_signed', models.CharField(max_length=50, null=True)),
                ('tel', models.CharField(max_length=50)),
                ('type_of_leave', models.CharField(choices=[('none', 'None'), ('sick leave', 'Sick Leave'), ('personal leave', 'Personal Leave'), ('annual leave', 'Annual Leave'), ('other', 'Other')], default='none', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Timesheets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.TimeField(default='00:00')),
                ('time_out', models.TimeField(default='-', null=True)),
                ('description', models.CharField(max_length=256)),
                ('type_of_work', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('who_signed', models.CharField(max_length=50, null=True)),
                ('type_sign', models.CharField(default='normal', max_length=50)),
                ('status', models.CharField(choices=[(0, 'rejected'), (1, 'pending'), (2, 'approved')], default=1, max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timesheets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]