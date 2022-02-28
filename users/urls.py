from django.urls import path
from .views import LoginView, StudentView, TeacherView, SuperAdminView,ResetPassword

urlpatterns = [
    path('login', LoginView.as_view()),
    path('password', ResetPassword.as_view()),
    path('student', StudentView.as_view()),
    path('teacher', TeacherView.as_view()),
    path('superadmin', SuperAdminView.as_view()),
]