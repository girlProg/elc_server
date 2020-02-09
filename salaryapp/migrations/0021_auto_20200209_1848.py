# Generated by Django 3.0.2 on 2020-02-09 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salaryapp', '0020_auto_20200209_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariableAdjustmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, default='', max_length=500, null=True)),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='variableadjustment',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='varadj', to='salaryapp.VariableAdjustmentType'),
        ),
    ]
