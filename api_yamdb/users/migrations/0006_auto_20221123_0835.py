# Generated by Django 2.2.16 on 2022-11-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20221123_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeemail',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]