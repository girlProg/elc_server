# Generated by Django 3.0.2 on 2020-02-09 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0016_auto_20200209_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='allowanceforHeads',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='grossIncome',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='nhis',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='salaryAmount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
