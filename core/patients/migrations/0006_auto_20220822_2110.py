# Generated by Django 3.2 on 2022-08-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_auto_20220822_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='end_visit_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='start_visit_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
