# Generated by Django 5.1.4 on 2024-12-11 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfinance', '0004_alter_income_total_income_alter_savings_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
