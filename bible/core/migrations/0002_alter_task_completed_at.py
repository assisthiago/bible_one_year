# Generated by Django 4.1.3 on 2022-12-23 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.TimeField(blank=True, null=True, verbose_name='concluído em'),
        ),
    ]
