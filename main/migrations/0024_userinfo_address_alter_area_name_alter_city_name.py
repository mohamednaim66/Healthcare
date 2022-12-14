# Generated by Django 4.0.4 on 2022-05-24 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_city_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.area'),
        ),
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, verbose_name='City'),
        ),
    ]
