# Generated by Django 3.0.2 on 2022-04-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0029_auto_20200805_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='month',
            field=models.CharField(blank=True, default='4', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='payslip',
            name='year',
            field=models.CharField(blank=True, default='2022', max_length=500, null=True),
        ),
    ]
