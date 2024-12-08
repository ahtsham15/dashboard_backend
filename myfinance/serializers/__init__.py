try:
    from .userSerializer import UserSerializer, LoginSerializer
    from .incomeSerializer import IncomeSerializer
    from .savingSerializer import SavingSerializer
    from .expenseSerializer import ExpenseSerializer
except ImportError:
    from rest_framework import serializers
    from myfinance.models import User, Income, Savings, Expense

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = '__all__'

    class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    class IncomeSerializer(serializers.ModelSerializer):
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        class Meta:
            model = Income
            fields = '__all__'

        date = serializers.DateField(required=False)
        source = serializers.CharField(max_length=100, required=False)
        description = serializers.CharField(required=False)
        total_income = serializers.DecimalField(max_digits=10, decimal_places=4, required=False)

    class SavingSerializer(serializers.ModelSerializer):
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        class Meta:
            model = Savings
            fields = '__all__'
        date = serializers.DateField(required=False)
        description = serializers.CharField(max_length=100, required=False)
        amount = serializers.DecimalField(max_digits=10, decimal_places=4, required=False)

    class ExpenseSerializer(serializers.ModelSerializer):
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        class Meta:
            model = Expense
            fields = '__all__'
        date = serializers.DateField(required=False)
        category = serializers.CharField(max_length=100, required=False)
        description = serializers.CharField(required=False)
        amount = serializers.DecimalField(max_digits=10, decimal_places=4, required=False)