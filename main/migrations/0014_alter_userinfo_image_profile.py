# Generated by Django 4.0.4 on 2022-05-21 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_userinfo_image_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='image_profile',
            field=models.ImageField(blank=True, default='image_profile/default_profile.jpg', null=True, upload_to='image_profile'),
        ),
    ]
