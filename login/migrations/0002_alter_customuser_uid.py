# Generated by Django 4.1.5 on 2023-03-12 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001891607FCE0>', max_length=200),
        ),
    ]
