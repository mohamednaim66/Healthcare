# Generated by Django 4.0.4 on 2022-05-28 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_patientregister'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(default='male', max_length=10),
        ),
    ]