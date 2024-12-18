from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from myfinance.models import User, Income, Savings, Expense
from decimal import Decimal
from myfinance.serializers import UserSerializer
from rest_framework import generics
from myfinance.serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        # You can add custom logic here if needed
        
        # Call the original `post` method from `CreateAPIView`
        response = self.create(request, *args, **kwargs)

        # Return the response explicitly
        return response

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
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                user = user
            else:
                user = None
        except User.DoesNotExist:
            user = None
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "User logged in successfully",
                "data": {
                    "user": user_serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": "Invalid credentials"
            },status=status.HTTP_401_UNAUTHORIZED)
        # print(data)
        # serializer = LoginSerializer(data=data)
        # if not serializer.is_valid():
        #     return Response({
        #         "status": False,
        #         "message": serializer.errors
        #     })
        # email = serializer.data['email']
        # password = serializer.data['password']
        # user = User.objects.filter(email=email).first()
        # print(user)
        # if not user:
        #     return Response({
        #         "status": False,
        #         "message": "User not found"
        #     })
        # return Response({
        #     "status": "success",
        #     "data":{}
        # })