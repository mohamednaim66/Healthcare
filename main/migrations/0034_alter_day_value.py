# Generated by Django 4.0.4 on 2022-05-30 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_day_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='value',
            field=models.IntegerField(unique=True),
        ),
    ]