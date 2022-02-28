from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
import jwt
import datetime

#User login Api to login users
class LoginView(APIView):
    def post(self, request):
        name = request.data['name']#used name and level for signup and login
        level=request.data['level']
        if level=='superadmin':#then created token for particular user
            user = SuperAdmin.objects.filter(name=name).first()
            if user is None:
                serializer = SuperAdminSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            user = SuperAdmin.objects.filter(name=name).first()

        elif level=='teacher':
            user = Teacher.objects.filter(name=name).first()
            if user is None:
                serializer = TeacherSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            user = Teacher.objects.filter(name=name).first()
        
        elif level=='student':
            user = Student.objects.filter(name=name).first()
            if user is None:
                serializer = StudentSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            user = Student.objects.filter(name=name).first()
       
        payload = {
            'id': user.id,
            'level': user.level,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        #token includes user id and level
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        time = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        response.data = {
            'jwt': token,
            'time': time
        }

        return response


#StudentApi for a particular student to view his details
class StudentView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        user = Student.objects.filter(id=payload['id']).first()
        if user.level == 'student':
            serializer = StudentSerializers(user)
            return Response(serializer.data)
        else:
            return Response({'message': 'You are not a student!'})

#TeacherApi for a particular teacher to add/list all students
class TeacherView(APIView):
    #Teacher can list/view students
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        if payload['level'] == 'teacher':
            user = Student.objects.all()
            serializer = StudentSerializers(user, many=True)
            return Response(serializer.data)
        
        else:
            return Response({'message': 'You are not a teacher!'})
        
    #Teacher can add students
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()
        if payload['level'] == 'teacher':
            if request.data['level'] == 'student':
                serializer=StudentSerializers(data=request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors)
                    
                serializer.save()
                response.data = {
                    'message': 'Successfully added new student!'
                }

            
            else:
                response.data = {
                    'message': 'Its not a student!'
                }

        else:
            response.data = {
                'message': 'You are not a teacher!'
            }
        return response

class SuperAdminView(APIView):
    #SuperAdmin can list/view all users
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        if payload['level'] == 'superadmin':
            user = Student.objects.all()
            user1=Teacher.objects.all()
            user2=SuperAdmin.objects.all()
            serializer = StudentSerializers(user, many=True)
            serializer1 = TeacherSerializers(user1, many=True)
            serializer2 = SuperAdminSerializers(user2, many=True)
            return Response({'students': serializer.data, 'teachers': serializer1.data, 'superadmins': serializer2.data})
        
        else:
            return Response({'message': 'You are not a superadmin!'})
        
    #SuperAdmin can add any user
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()
        if payload['level'] == 'superadmin':
            if request.data['level'] == 'student':
                serializer=StudentSerializers(data=request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors)
                    
                serializer.save()
                response.data = {
                    'message': 'Successfully added new student!'
                }
            elif request.data['level'] == 'teacher':
                serializer=TeacherSerializers(data=request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors)
                    
                serializer.save()
                response.data = {
                    'message': 'Successfully added new teacher!'
                }
            
            elif request.data['level'] == 'superadmin':
                serializer=SuperAdminSerializers(data=request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors)
                    
                serializer.save()
                response.data = {
                    'message': 'Successfully added new superadmin!'
                }
        
            else:
                response.data = {
                    'message': 'Invalid user!'
                }
                return response
        else:
            response.data = {
                'message': 'You are not a superadmin!'
            }
        return response

#ResetPasswordApi for a particular user to reset password
class ResetPassword(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()

        if payload['level'] == 'student':
            user=Student.objects.filter(id=payload['id']).first()
            user.password=request.data['password']
            user.save()
            response.data = {
                'message': 'Successfully added new password!'
            }
        elif payload['level'] == 'teacher':
            user=Teacher.objects.filter(id=payload['id']).first()
            user.password=request.data['password']
            user.save()
            response.data = {
                'message': 'Successfully added new password!'
            }    
            
        elif payload['level'] == 'superadmin':
            user=SuperAdmin.objects.filter(id=payload['id']).first()
            user.password=request.data['password']
            user.save()
            response.data = {
                'message': 'Successfully added new password!'
            }

        else:
            response.data = {
                'message': 'Invalid user!'
            }
        return response

        

    