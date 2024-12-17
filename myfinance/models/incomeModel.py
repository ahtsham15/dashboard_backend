from django.db import models
from myfinance.models import User

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    total_income = models.DecimalField(max_digits=10, decimal_places=4, default=0)
