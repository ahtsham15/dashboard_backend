from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .models import Income
from .serializers import UserSerializer,LoginSerializer,IncomeSerializer
from rest_framework import status
# Create your views here.
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
    
class IncomeList(APIView):
    def post(self, request):
        try:
            if 'user' not in request.data:
                return Response({
                    "status": False,
                    "message": "User ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            user_id = request.data.get('user')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    "status": False, 
                    "message": "User does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
            amount = request.data.get('amount')
            if amount and float(amount) <= 0:
                return Response({
                    "status": False,
                    "message": "Amount must be greater than 0"
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = IncomeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Income created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": False,
                    "errors": serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class IncomeDetail(APIView):
    def get(self, request, pk):
        try:
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "User does not exist"
                }, status=status.HTTP_404_NOT_FOUND)

            incomes = Income.objects.filter(user=user)
            
            if not incomes.exists():
                return Response({
                    "status": True,
                    "message": "No income records found for this user",
                    "data": []
                }, status=status.HTTP_200_OK)

            serializer = IncomeSerializer(incomes, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def patch(self, request, pk):
        try:
            try:
                income = Income.objects.get(id=pk)
            except Income.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "Income does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
            print(request.data)
            serializer = IncomeSerializer(income, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  
                return Response({
                    "status": True,
                    "message": "Income updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            income = Income.objects.get(id=pk)
            income.delete()
            return Response({
                "status": True,
                "message": "Income deleted successfully"
            }) 
        except Income.DoesNotExist:
            return Response({
                "status": False,
                "message": "Income does not exist"
            }, status=status.HTTP_404_NOT_FOUND)