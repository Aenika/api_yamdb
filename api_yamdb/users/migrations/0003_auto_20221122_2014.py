# Generated by Django 2.2.16 on 2022-11-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221122_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeemail',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
