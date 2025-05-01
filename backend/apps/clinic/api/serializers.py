from rest_framework import serializers
from apps.clinic.models import Staff, Patient, Appointment, PhoneNumber, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    role = RoleSerializer()
    class Meta:
        model = Staff
        fields = '__all__'

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    staff = StaffSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'
