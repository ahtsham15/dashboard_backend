# Generated by Django 5.1.4 on 2024-12-11 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfinance', '0005_alter_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]