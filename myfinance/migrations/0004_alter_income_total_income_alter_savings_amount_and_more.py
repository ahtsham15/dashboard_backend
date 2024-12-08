# Generated by Django 5.1.4 on 2024-12-07 19:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfinance', '0003_income_total_income_savings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='total_income',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='savings',
            name='amount',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myfinance.user')),
            ],
        ),
    ]
