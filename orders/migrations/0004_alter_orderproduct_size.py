# Generated by Django 4.1.5 on 2023-03-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderproduct_sizevariant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='size',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
