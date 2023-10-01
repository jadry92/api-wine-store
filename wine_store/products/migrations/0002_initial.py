# Generated by Django 4.2.4 on 2023-09-30 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="productreview",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="discount",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="products.productdiscount",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="inventory",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name="product", to="products.productinventory"
            ),
        ),
    ]
