# Generated by Django 3.0.2 on 2022-04-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('chat_id', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('email_pw', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('uid', models.CharField(blank=True, default='', max_length=500, null=True)),
            ],
            options={
                'ordering': ['-modified'],
                'abstract': False,
            },
        ),
    ]
