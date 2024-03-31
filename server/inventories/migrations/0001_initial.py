# Generated by Django 5.0.3 on 2024-03-31 01:17

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('low_stock_threshold', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('out_of_stock_threshold', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('stock', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.status')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventories.type')),
            ],
        ),
    ]