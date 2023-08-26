# Generated by Django 4.2.4 on 2023-08-16 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="product",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="products.product"),
        ),
    ]