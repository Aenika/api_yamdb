# Generated by Django 2.2.16 on 2022-11-23 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20221123_0835'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CodeEmail',
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]