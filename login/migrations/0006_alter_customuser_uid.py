# Generated by Django 4.1.5 on 2023-03-15 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_customuser_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000002510AD7FCE0>', max_length=200),
        ),
    ]
