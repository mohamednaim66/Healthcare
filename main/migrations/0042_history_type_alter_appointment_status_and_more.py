# Generated by Django 4.0.4 on 2022-07-12 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0041_appointment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='History_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'accepted'), (2, 'pended'), (3, 'rejected')], default=2),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Info', to=settings.AUTH_USER_MODEL),
        ),
    ]
