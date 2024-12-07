from django.db import models
from myfinance.models import User

class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()
    description = models.TextField()