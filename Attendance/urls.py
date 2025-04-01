"""
URL configuration for Attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from faceRecAttendance import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.users, name='users'),
    path('pic/<str:user_id>/', views.pic, name='single_user'),
    path('user/', views.user, name='single_user'),
    path("register/", views.register_user, name="register-user"),
    path("mark-attendance/", views.mark_attendance, name="mark-attendance"),
    path("attendance-records/", views.get_attendance_records, name="attendance-records"),
    path('details/<str:user_id>/', views.user_details, name='details'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
