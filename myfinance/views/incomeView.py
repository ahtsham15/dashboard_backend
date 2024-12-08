from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from myfinance.models import User, Income, Savings, Expense
from rest_framework import status
from decimal import Decimal
from myfinance.serializers import (
    IncomeSerializer, 
)

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
            
            previous_incomes = Income.objects.filter(user=user)
            total_income = sum(income.amount for income in previous_incomes)  # Sum all the amounts
            total_income += Decimal(amount) 
            new_income_data = {
                "user": user.id,
                "amount": Decimal(amount),
                "total_income": total_income,
                "date": request.data.get('date'),
                "source": request.data.get('source'),
                "description": request.data.get('description')
            }
            
            serializer = IncomeSerializer(data=new_income_data)
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