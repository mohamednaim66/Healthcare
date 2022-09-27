# Generated by Django 4.0.4 on 2022-07-29 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_alter_patientregister_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='ex_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'accepted'), (2, 'pended'), (3, 'rejected'), (4, 'Attended'), (5, 'Not attended')], default=2),
        ),
        migrations.AlterField(
            model_name='patientregister',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='main.userinfo'),
        ),
    ]
