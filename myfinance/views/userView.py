from rest_framework.views import APIView
from rest_framework.response import Response
from myfinance.models import User
from myfinance.serializers import UserSerializer, LoginSerializer

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        })
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": serializer.errors
            })
        serializer.save()
        return Response({
            "status": True,
            "message": "User created successfully"
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
        email = serializer.data['email']
        password = serializer.data['password']
        user = User.objects.filter(email=email).first()
        print(user)
        if not user:
            return Response({
                "status": False,
                "message": "User not found"
            })
        return Response({
            "status": "success",
            "data":{}
        })