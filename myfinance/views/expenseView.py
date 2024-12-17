from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from myfinance.models import User, Income, Savings, Expense
from rest_framework import status
import csv
import os
from django.conf import settings
from django.http import JsonResponse
from io import StringIO
from django.http import HttpResponse
from io import StringIO
from decimal import Decimal
from myfinance.serializers import (
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
            user = User.objects.get(id=request.data.get('user'))
            amount = Decimal(request.data.get("amount",0))
            latest_income = Income.objects.filter(user=user).last()
            if not latest_income:
                return Response({
                    "status":False,
                    "message":"No Income record found for the user"
                },status=status.HTTP_400_BAD_REQUEST)
            total_income = latest_income.total_income
            amount_difference = amount-total_income
            if amount_difference > 0 and float(total_income) < float(amount_difference):
                return Response({
                    "status": False,
                    "message": 'Insufficient balance'
                },status=status.HTTP_400_BAD_REQUEST)
            
            new_total_income = total_income - amount_difference
            latest_income.total_income = new_total_income
            latest_income.save()
            serializer = ExpenseSerializer(expense, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Expense update Successfully"
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "message": serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occured: {str(e)}"
            },status=status.HTTP_400_BAD_REQUEST) 
    
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
        
class ExpenseCSV(APIView):
    def get(self, request, pk):
        try:
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "User does not exist"
                }, status=status.HTTP_404_NOT_FOUND)
            expenses = Expense.objects.filter(user=user).order_by('date')

            if not expenses.exists():
                return Response({
                    "status": False,
                    "message": "No expenses found for this user"
                }, status=status.HTTP_404_NOT_FOUND)
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])
            for expense in expenses:
                writer.writerow([
                    expense.date,
                    expense.category,
                    expense.amount,
                    expense.description
                ])
            file_name = f"expenses_{user.id}_{expenses.first().date.strftime('%Y_%m')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, 'expense_reports', file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as csv_file:
                csv_file.write(csv_buffer.getvalue())

            return JsonResponse({
                "status": True,
                "message": "CSV file created successfully",
                "file_path": file_path
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)