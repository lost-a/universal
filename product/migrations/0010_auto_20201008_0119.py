# Generated by Django 3.1.1 on 2020-10-08 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_purchase_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
