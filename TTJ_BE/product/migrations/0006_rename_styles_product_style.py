# Generated by Django 5.0.6 on 2024-07-04 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='styles',
            new_name='style',
        ),
    ]