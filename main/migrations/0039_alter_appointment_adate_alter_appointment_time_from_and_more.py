# Generated by Django 4.0.4 on 2022-06-01 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_alter_appointment_adate_alter_appointment_time_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='adate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time_from',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time_to',
            field=models.TimeField(),
        ),
    ]