# Generated by Django 5.0.6 on 2024-07-04 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='styles', to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.FloatField()),
                ('name', models.CharField(max_length=300)),
                ('rating', models.JSONField(default=dict)),
                ('priceCents', models.IntegerField()),
                ('keywords', models.JSONField(default=list)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category')),
                ('styles', models.ManyToManyField(related_name='products', to='product.style')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='style',
            field=models.ManyToManyField(related_name='categories', to='product.style'),
        ),
    ]
