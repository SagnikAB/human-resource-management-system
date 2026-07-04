from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from .validators import validate_strong_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'employee_id', 'email', 'role', 'is_active', 'date_joined')
        read_only_fields = ('id', 'employee_id', 'is_active', 'date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_strong_password])
    employee_id = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('employee_id', 'email', 'password', 'role')

    def validate_role(self, value):
        request = self.context.get('request')
        if value in [CustomUser.Role.ADMIN, CustomUser.Role.HR] and (not request or not request.user.is_authenticated or not request.user.is_admin_or_hr):
            raise serializers.ValidationError('Only administrators can create admin or HR users.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        return CustomUser.objects.create_user(password=password, **validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')
        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_strong_password])

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
