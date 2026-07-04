from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import AttendanceRecord, Employee, LeaveRequest, PayrollRecord, SalaryStructure

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    employee_id = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Employee.Role.choices, default=Employee.Role.EMPLOYEE)
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True)
    designation = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def validate_employee_id(self, value):
        if Employee.objects.filter(employee_code=value).exists():
            raise serializers.ValidationError("An employee with this ID already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        employee_code = validated_data.pop("employee_id")
        email = validated_data.pop("email")
        role = validated_data.pop("role")
        user = User.objects.create_user(username=email, email=email, password=password)
        if role in {Employee.Role.ADMIN, Employee.Role.HR}:
            user.is_staff = True
            user.save(update_fields=["is_staff"])
        Employee.objects.create(user=user, employee_code=employee_code, role=role, **validated_data)
        return user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower()
        user = authenticate(username=email, password=attrs["password"])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_code",
            "email",
            "role",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "address",
            "date_of_birth",
            "profile_picture_url",
            "department",
            "designation",
            "joining_date",
            "manager",
            "employment_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class EmployeeSelfUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["phone", "address", "profile_picture_url"]


class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            "id",
            "employee",
            "employee_name",
            "work_date",
            "check_in_at",
            "check_out_at",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)
    reviewer_email = serializers.EmailField(source="reviewer.email", read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "start_date",
            "end_date",
            "remarks",
            "status",
            "reviewer",
            "reviewer_email",
            "reviewer_note",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "reviewer", "reviewer_note", "reviewed_at", "created_at", "updated_at"]

    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError({"end_date": "End date must be on or after start date."})
        return attrs


class LeaveDecisionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[LeaveRequest.Status.APPROVED, LeaveRequest.Status.REJECTED])
    reviewer_note = serializers.CharField(required=False, allow_blank=True)


class SalaryStructureSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = SalaryStructure
        fields = [
            "id",
            "employee",
            "employee_name",
            "base_salary",
            "hra",
            "allowances",
            "deductions",
            "effective_from",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["is_active", "created_at", "updated_at"]


class PayrollRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = PayrollRecord
        fields = [
            "id",
            "employee",
            "employee_name",
            "year",
            "month",
            "gross_pay",
            "deductions",
            "net_pay",
            "generated_at",
            "published_at",
        ]
        read_only_fields = ["generated_at"]
