# Generated by Django 3.0.1 on 2019-12-21 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0002_bankaccount_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='name',
        ),
    ]
