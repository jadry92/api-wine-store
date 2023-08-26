# Generated by Django 4.2.4 on 2023-08-26 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productreview",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="products.product"
            ),
        ),
    ]