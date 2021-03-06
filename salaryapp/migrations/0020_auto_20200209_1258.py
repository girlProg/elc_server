# Generated by Django 3.0.2 on 2020-02-09 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0019_auto_20200209_1251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='negatives',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='pension',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='positives',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='sbasic',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='sdomestic',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='sdressing',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='seducation',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='sentertainment',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='smeal',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='stransport',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RenameField(
            model_name='sutility',
            old_name='salary',
            new_name='payslip',
        ),
        migrations.RemoveField(
            model_name='shousing',
            name='salary',
        ),
        migrations.AddField(
            model_name='shousing',
            name='payslip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='housing', to='salaryapp.PaySlip'),
        ),
    ]
