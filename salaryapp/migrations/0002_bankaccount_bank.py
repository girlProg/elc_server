# Generated by Django 3.0.1 on 2019-12-21 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='bank',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='bank', to='salaryapp.Bank'),
        ),
    ]
