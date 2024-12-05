from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer,LoginSerializer
# Create your views here.
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        })
    

class LoginView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": serializer.errors
            })
        return Response({
            "status": "success",
            "data":{}
        })