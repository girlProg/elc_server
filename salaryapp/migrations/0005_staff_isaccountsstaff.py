# Generated by Django 3.0.1 on 2019-12-21 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0004_auto_20191221_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='isAccountsStaff',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
