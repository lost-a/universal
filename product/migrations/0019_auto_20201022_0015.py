# Generated by Django 3.1.1 on 2020-10-22 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_auto_20201021_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='duration_type',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
