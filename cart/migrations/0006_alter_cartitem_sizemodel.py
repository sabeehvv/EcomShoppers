# Generated by Django 4.1.5 on 2023-03-30 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_sizevariant_stock"),
        ("cart", "0005_cartitem_sizemodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="sizemodel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="products.sizevariant",
            ),
        ),
    ]