# Generated by Django 3.2.6 on 2021-10-31 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mastersheet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='read',
            field=models.CharField(default='none', max_length=10),
        ),
    ]