# Generated by Django 3.2.20 on 2023-08-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='pay',
            field=models.BooleanField(default=False),
        ),
    ]