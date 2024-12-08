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
    ExpenseSerializer,
)

from decimal import Decimal

class ExpenseList(APIView):
    def post(self, request):
        try:
            if 'user' not in request.data:
                return Response({
                    "status": False,
                    "message": "User ID is required",
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_id = request.data.get('user')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "User does not exist",
                }, status=status.HTTP_404_NOT_FOUND)
            
            amount = request.data.get('amount')
            if amount and float(amount) <= 0:
                return Response({
                    "status": False,
                    "message": "Amount must be greater than 0",
                }, status=status.HTTP_400_BAD_REQUEST)
            
            latest_income = Income.objects.filter(user=user).last()
            if not latest_income:
                return Response({
                    "status": False,
                    "message": "No income record found for the user",
                }, status=status.HTTP_404_NOT_FOUND)

            total_income = latest_income.total_income
            # Convert amount to Decimal
            amount = Decimal(amount)
            if total_income < amount:
                return Response({
                    "status": False,
                    "message": "Insufficient funds",
                }, status=status.HTTP_400_BAD_REQUEST)
            
            new_total_income = total_income - amount
            latest_income.total_income = new_total_income
            latest_income.save()
            
            serializer = ExpenseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Expense created successfully",
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": False,
                    "message": serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExpenseDetail(APIView):
    def get(self, request, pk):
        try:
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "User does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
            expense = Expense.objects.filter(user=user)
            if not expense.exists():
                return Response({
                    "status": True,
                    "message": "No expense records found for this user",
                    "data": []
                }, status=status.HTTP_200_OK)
            serializer = ExpenseSerializer(expense, many=True)
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
                expense = Expense.objects.get(id=pk)
            except Expense.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "Expense does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
            print("User ID:", expense.user_id)
            if expense.amount < Decimal(request.data.get("amount", 0)):
                user = User.objects.get(id=request.data.get("user"))
                serializer = ExpenseSerializer(expense, data=request.data, partial=True)
                amount = request.data.get("amount")
                latest_income = Income.objects.filter(user=user).last()
                print("Income:",latest_income)
                total_income = latest_income.total_income
                amount = Decimal(amount)
                if float(total_income) < float(amount):
                    return Response({
                        "status": False,
                        "message": "Insufficient balance"
                    }, status=status.HTTP_400_BAD_REQUEST)
                new_total_income = total_income - amount
                latest_income.total_income = new_total_income
                latest_income.save()
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "status": True,
                        "message": "Expense updated successfully",
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": False,
                    "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.get(id=request.data.get("user"))
                serializer = ExpenseSerializer(expense, data=request.data, partial=True)
                amount = request.data.get("amount")
                latest_income = Income.objects.filter(user=user).last()
                print("Income:",latest_income)
                total_income = latest_income.total_income
                amount = Decimal(amount)
                new_amount = expense.amount - amount
                new_amount = Decimal(new_amount)
                if float(total_income) < float(new_amount):
                    return Response({
                        "status": False,
                        "message": "Insufficient balance"
                    }, status=status.HTTP_400_BAD_REQUEST)
                new_total_income = total_income + new_amount
                latest_income.total_income = new_total_income
                latest_income.save()
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "status": True,
                        "message": "Expense updated successfully",
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": False,
                        "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            expensee = Expense.objects.get(id=pk)
            expensee.delete()
            return Response({
                "status": True,
                "message": "Expense deleted successfully"
            })
        except Expense.DoesNotExist:
            return Response({
                "status": False,
                "message": "Expense does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)