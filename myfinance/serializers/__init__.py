try:
    # from .userSerializer import UserSerializer
    from .incomeSerializer import IncomeSerializer
    from .savingSerializer import SavingSerializer
    from .expenseSerializer import ExpenseSerializer
except ImportError:
    from rest_framework import serializers
    from myfinance.models import User, Income, Savings, Expense
    from django.contrib.auth.hashers import make_password

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields =['id', 'username', 'email', 'password']


    class RegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['username', 'email', 'password']
        def create(self, validated_data):
            user = User(
                username=validated_data['username'],
                email=validated_data['email'],
                password=make_password(validated_data['password'])  # Hash the password directly
            )
            user.save()
            return user
        
    # class LoginSerializer(serializers.Serializer):
    #     email = serializers.EmailField(required=True)
    #     password = serializers.CharField(required=True, write_only=True)

    class LoginSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True)
        
        class Meta:
            model = User
            fields = ['email', 'password']

    class IncomeSerializer(serializers.ModelSerializer):
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        description = serializers.CharField(allow_null=True, required=False)
        class Meta:
            model = Income
            fields = '__all__'

        date = serializers.DateField(required=False)
        source = serializers.CharField(max_length=100, required=False)
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