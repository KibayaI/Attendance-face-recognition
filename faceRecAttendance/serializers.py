from rest_framework import serializers
from .models import User, AttendanceRecord
import bcrypt


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            # 'password': {'write_only': True},
            'user_id': {'read_only': True}
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        hashed_password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()
        validated_data['password'] = hashed_password
        return User.objects.create(**validated_data)


class AttendanceRecordSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AttendanceRecord
        fields = ['attendance_id', 'attendance_date', 'time_slot', 'status', 'user']

