# Generated by Django 3.0.2 on 2020-08-05 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0028_auto_20200229_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='month',
            field=models.CharField(blank=True, default='8', max_length=500, null=True),
        ),
    ]