from django.db.models import fields
from rest_framework import serializers
from .models import SuperAdmin, Teacher, Student

#Created modelSerializer for each user

class SuperAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = '__all__'


class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

