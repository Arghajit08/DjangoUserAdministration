from django.contrib import admin
#imported all model class and register them in admin
from .models import SuperAdmin, Teacher, Student

admin.site.register(SuperAdmin)
admin.site.register(Teacher)
admin.site.register(Student)

# Register your models here.
