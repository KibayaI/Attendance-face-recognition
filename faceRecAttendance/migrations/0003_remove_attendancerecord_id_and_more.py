# Generated by Django 5.0.13 on 2025-04-01 13:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceRecAttendance', '0002_user_face_embedding_attendancerecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancerecord',
            name='id',
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='attendance_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='status',
            field=models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('excused', 'Excused')], default='present', max_length=10),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='time_slot',
            field=models.CharField(choices=[('07:00-10:00', '7:00 AM - 10:00 AM'), ('11:00-14:00', '11:00 AM - 2:00 PM'), ('15:00-18:00', '3:00 PM - 6:00 PM')], max_length=20),
        ),
        migrations.AddIndex(
            model_name='attendancerecord',
            index=models.Index(fields=['attendance_date', 'time_slot'], name='faceRecAtte_attenda_b75852_idx'),
        ),
    ]
