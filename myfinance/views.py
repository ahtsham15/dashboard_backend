from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from .models import User
from .models import Income
from .models import Savings
from .serializers import UserSerializer,LoginSerializer,IncomeSerializer,SavingSerializer
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
