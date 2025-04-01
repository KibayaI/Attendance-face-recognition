import bcrypt
import numpy as np
from django.utils.timezone import now
from .serializers import UserSerializer
import face_recognition
from .models import User, AttendanceRecord
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def users(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"Error": "Email already in use!"})

        return Response(serializer.data)
    elif request.method == 'GET':
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        all_users = User.objects.all()
        all_users.delete()

        return Response("All are goners!!!")


@api_view(['GET', 'POST'])
def pic(request, user_id):
    if request.method == 'GET':
        try:
            single_user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(single_user, many=False)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        return Response(serializer.data)


@api_view(['GET'])
def user_details(request, user_id):
    try:
        details = AttendanceRecord.objects.filter(user_id=user_id)
        serializer = AttendanceRecordSerializer(details, many=True)
    except AttendanceRecord.DoesNotExist:
        return Response({"error": "User does not exist"}, status=404)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['POST'])
def user(request):
    email = request.data['email']
    password = request.data['password']

    try:
        if_email_exist = User.objects.get(email=email)
        serializer = UserSerializer(if_email_exist, many=False)

        if bcrypt.checkpw(password.encode(), serializer.data['password'].encode()):
            return Response({"Success": "Proceed to app",
                             "user_id": serializer.data['user_id']})
        else:
            return Response({"Error": "Incorrect Password"})

    except User.DoesNotExist:
        return Response({"Error": "Email does not exist"})


@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        # Use the serializer to validate and save the user data
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save user after password hashing
            return Response({
                "message": "User registered successfully",
                "user_id": serializer.data["user_id"],
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def mark_attendance(request):
    if 'image' not in request.FILES:
        return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_image = request.FILES['image']
    image = face_recognition.load_image_file(uploaded_image)
    uploaded_encoding = face_recognition.face_encodings(image)

    if not uploaded_encoding:
        return Response({"error": "No face detected"}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_encoding = uploaded_encoding[0]
    users = User.objects.exclude(face_embedding=None)

    for user in users:
        stored_encoding = np.frombuffer(user.face_embedding, dtype=np.float64)
        match = face_recognition.compare_faces([stored_encoding], uploaded_encoding, tolerance=0.5)

        if match[0]:
            time_slot = AttendanceRecord.get_current_time_slot()
            if time_slot:
                attendance, created = AttendanceRecord.objects.get_or_create(
                    user=user,
                    attendance_date=now().date(),
                    time_slot=time_slot,
                    defaults={'status': 'present'}
                )

                if not created:
                    return Response({"message": f"Attendance already marked for {user.name} ({time_slot})"},
                                    status=status.HTTP_200_OK)

                return Response({
                    "message": f"Attendance marked for {user.name} ({time_slot})",
                    "attendance_id": attendance.attendance_id
                }, status=status.HTTP_201_CREATED)

            return Response({"error": "Outside allowed attendance hours"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Face not recognized"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_attendance_records(request):
    records = AttendanceRecord.objects.select_related('user').filter(user__role='student')
    serializer = AttendanceRecordSerializer(records, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)
