# Generated by Django 3.2.20 on 2023-10-03 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_alter_historico_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='checkOut',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
