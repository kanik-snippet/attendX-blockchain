from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Teacher, Student

# CustomUser Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_teacher', 'is_student']

# Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = [
            'user', 'first_name', 'last_name', 'department', 'subjects',
            'total_lectures_given', 'total_students_present', 'total_students_absent'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['password'] = make_password(user_data.pop('password'))  # Hash password
        user = CustomUser.objects.create(**user_data, is_teacher=True)

        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Student
        fields = [
            'user', 'first_name', 'last_name', 'department', 'branch', 'year', 'semester', 'profile_photo',
            'lectures_attended_today', 'lectures_attended_week', 'lectures_attended_month', 'lectures_attended_semester'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['password'] = make_password(user_data.pop('password'))  # Hash password
        user = CustomUser.objects.create(**user_data, is_student=True)

        student = Student.objects.create(user=user, **validated_data)
        return student


# Unified Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['teacher', 'student'], write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    department = serializers.CharField(required=True)

    # Teacher-specific fields
    subjects = serializers.CharField(required=False, allow_blank=True)

    # Student-specific fields
    branch = serializers.CharField(required=False, allow_blank=True)
    year = serializers.IntegerField(required=False, default=1)
    semester = serializers.IntegerField(required=False, default=1)
    profile_photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'password', 'role',
            'first_name', 'last_name', 'department', 'subjects',
            'branch', 'year', 'semester', 'profile_photo'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Extract common user fields
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': make_password(password),
            'is_teacher': role == 'teacher',
            'is_student': role == 'student'
        }

        # Create User
        user = CustomUser.objects.create(**user_data)

        # Create Teacher profile
        if role == 'teacher':
            Teacher.objects.create(
                user=user,
                first_name=validated_data.pop('first_name'),
                last_name=validated_data.pop('last_name'),
                department=validated_data.pop('department'),
                subjects=validated_data.pop('subjects', '')
            )

        # Create Student profile
        elif role == 'student':
            Student.objects.create(
                user=user,
                first_name=validated_data.pop('first_name'),
                last_name=validated_data.pop('last_name'),
                department=validated_data.pop('department'),
                branch=validated_data.pop('branch', ''),
                year=validated_data.pop('year', 1),
                semester=validated_data.pop('semester', 1),
                profile_photo=validated_data.pop('profile_photo', None)
            )

        return user

from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not check_password(password, user.password):  # 🔥 Check hashed password
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is not active")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_teacher': user.is_teacher,
                'is_student': user.is_student,
            }
        }
