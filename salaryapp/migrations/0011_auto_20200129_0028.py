# Generated by Django 3.0.2 on 2020-01-29 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0010_auto_20200128_2350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payslip',
            options={'ordering': ['-modified']},
        ),
        migrations.AlterUniqueTogether(
            name='payslip',
            unique_together=set(),
        ),
    ]
