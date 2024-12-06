from rest_framework import serializers
from .models import User
from .models import Income

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
    # user = serializers.IntegerField(required=False)  # Optional if updating without the user field
