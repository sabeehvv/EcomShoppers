# Generated by Django 4.1.5 on 2023-03-16 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_alter_customuser_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000002CDBD07FCE0>', max_length=200),
        ),
    ]
