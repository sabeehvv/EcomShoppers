# Generated by Django 4.1.5 on 2023-03-17 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='size',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
