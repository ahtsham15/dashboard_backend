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