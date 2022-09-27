# Generated by Django 4.0.4 on 2022-05-12 03:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_userinfo_phonenum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='PhoneNum',
            field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='invalid_password', message='Phone number must start 05 and it 10 digit like 05xxxxxxxx', regex='^05[0-9]{8}$')]),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]