from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from myfinance.models import User, Income, Savings, Expense
from rest_framework import status
from decimal import Decimal
from myfinance.serializers import (
    UserSerializer, 
    LoginSerializer, 
    IncomeSerializer, 
    SavingSerializer,
)

class SavingList(APIView):
    def post(self, request):
        try:
            try:
                user = User.objects.get(id=request.data.get('user'))
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
            latest_income = Income.objects.filter(user=user).last()
            if not latest_income:
                return Response({
                    "status": False,
                    "message": "No income records found for this user"
                }, status=status.HTTP_400_BAD_REQUEST)
            total_income = latest_income.total_income
            if total_income is None:
                total_income = 0.0  

            if float(total_income) < float(amount):
                return Response({
                    "status": False,
                    "message": "Insufficient balance"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print("TOTATL AMOUNT:",total_income)

            remaining_income = float(total_income) - float(amount)
            latest_income.total_income = remaining_income
            print(latest_income.total_income)
            latest_income.save()

            saving = Savings.objects.create(
                user=user,
                amount=amount,
                date=request.data.get('date'),
                description=request.data.get('description')
            )

            # Serialize the saving instance
            saving_serializer = SavingSerializer(saving)

            return Response({
                "status": True,
                "message": "Saving created successfully",
                "data": saving_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SavingDetail(APIView):
    def get(self, request, pk):
        try:
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "User does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
            savings = Savings.objects.filter(user=user)
            if not savings.exists():
                return Response({
                    "status": True,
                    "message": "No savings records found for this user",
                    "data": []
                }, status=status.HTTP_200_OK)
            serializer = SavingSerializer(savings, many=True)
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
                saving = Savings.objects.get(id=pk)  # Corrected line
            except Savings.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "Savings does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
        
            user = User.objects.get(id=request.data.get('user'))
        
            serializer = SavingSerializer(saving, data=request.data, partial=True)  # Note: `partial=True` (corrected casing)
        
            amount = request.data.get('amount')
            latest_income = Income.objects.filter(user=user).last()
        
            if not latest_income:
                return Response({
                    "status": False,
                "message": "No income records found for this user"
            }, status=status.HTTP_400_BAD_REQUEST)

            total_income = latest_income.total_income
            if total_income is None:
                total_income = 0.0  

            if float(total_income) < float(amount):
                return Response({
                    "status": False,
                    "message": "Insufficient balance"
                }, status=status.HTTP_400_BAD_REQUEST)

            print("TOTAL AMOUNT:", total_income)

            remaining_income = float(total_income) - float(amount)
            latest_income.total_income = remaining_income
            print(latest_income.total_income)
            latest_income.save()

            if serializer.is_valid():
                serializer.save()

            return Response({
                "status": True,
            "message": "Savings updated successfully",
            "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
            "status": False,
            "message": f"An error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            saving = Savings.objects.get(id=pk)
            if saving:
                saving.delete()
                return Response({
                    "status": True,
                    "message": "Savings deleted successfully"
                })
            else:
                return Response({
                    "status": False,
                    "message": "Savings does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
        except Savings.DoesNotExist:
            return Response({
                "status": False,
                "message": "Saving does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
