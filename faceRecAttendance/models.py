import os
import face_recognition
from django.db import models
import uuid
from datetime import date, datetime, time


class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]

    user_id = models.CharField(max_length=254, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=35)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=254)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='student')
    photo = models.ImageField(upload_to='images/')
    face_embedding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            file_path = self.photo.path

            if os.path.exists(file_path):
                image = face_recognition.load_image_file(file_path)
                encoding = face_recognition.face_encodings(image)

                if encoding:
                    self.face_embedding = encoding[0].tobytes()
                    super().save(update_fields=['face_embedding'])


class AttendanceRecord(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'
    LATE = 'late'
    EXCUSED = 'excused'

    ATTENDANCE_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
        (EXCUSED, 'Excused'),
    ]

    TIME_SLOTS = [
        ('07:00-10:00', '7:00 AM - 10:00 AM'),
        ('11:00-14:00', '11:00 AM - 2:00 PM'),
        ('15:00-18:00', '3:00 PM - 6:00 PM'),
    ]

    attendance_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    attendance_date = models.DateField(default=date.today)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default=PRESENT)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'attendance_date', 'time_slot')
        indexes = [models.Index(fields=['attendance_date', 'time_slot'])]

    def __str__(self):
        return f"{self.user.name} - {self.status} on {self.attendance_date} ({self.time_slot})"

    @staticmethod
    def get_current_time_slot():
        current_time = datetime.now().time()

        if time(7, 0) <= current_time < time(10, 0):
            return '07:00-10:00'
        elif time(11, 0) <= current_time < time(14, 0):
            return '11:00-14:00'
        elif time(15, 0) <= current_time < time(18, 0):
            return '15:00-18:00'
        return None
