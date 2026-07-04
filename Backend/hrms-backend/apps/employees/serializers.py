from rest_framework import serializers
from apps.authentication.models import CustomUser
from apps.authentication.serializers import UserSerializer
from .models import Department, EmployeeProfile

class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source='head.full_name', read_only=True)
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'head', 'head_name', 'created_at')
        read_only_fields = ('created_at',)

class EmployeeProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    class Meta:
        model = EmployeeProfile
        fields = ('id', 'user', 'first_name', 'last_name', 'phone', 'city', 'country', 'department', 'department_name', 'designation', 'employment_type', 'profile_picture')

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    role = serializers.ChoiceField(choices=CustomUser.Role.choices, write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    bank_account_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    manager_name = serializers.CharField(source='manager.full_name', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = ('id', 'user', 'email', 'role', 'password', 'first_name', 'last_name', 'phone', 'address', 'city', 'country', 'date_of_birth', 'gender', 'department', 'department_name', 'designation', 'date_of_joining', 'employment_type', 'manager', 'manager_name', 'profile_picture', 'emergency_contact_name', 'emergency_contact_phone', 'bank_account_number', 'bank_name', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get('request')
        if request and not request.user.is_admin_or_hr:
            admin_fields = {'department', 'designation', 'date_of_joining', 'employment_type', 'manager', 'bank_name'}
            if any(field in attrs for field in admin_fields):
                raise serializers.ValidationError('Employees cannot modify admin-controlled fields.')
        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', 'Employee@123')
        role = validated_data.pop('role', CustomUser.Role.EMPLOYEE)
        bank_account_number = validated_data.pop('bank_account_number', '')
        if not email:
            raise serializers.ValidationError({'email': 'Email is required when creating an employee.'})
        user = CustomUser.objects.create_user(email=email, password=password, role=role)
        profile = EmployeeProfile(user=user, **validated_data)
        profile.set_bank_account_number(bank_account_number)
        profile.save()
        return profile

    def update(self, instance, validated_data):
        validated_data.pop('email', None); validated_data.pop('role', None); validated_data.pop('password', None)
        bank_account_number = validated_data.pop('bank_account_number', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if bank_account_number is not None:
            instance.set_bank_account_number(bank_account_number)
        instance.save()
        return instance

class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ('profile_picture',)
