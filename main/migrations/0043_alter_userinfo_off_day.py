# Generated by Django 4.0.4 on 2022-07-25 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_history_type_alter_appointment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='off_day',
            field=models.ManyToManyField(blank=True, related_name='m', to='main.day'),
        ),
    ]
