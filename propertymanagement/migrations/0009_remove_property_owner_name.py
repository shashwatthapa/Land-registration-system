# Generated by Django 5.1.4 on 2025-02-09 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propertymanagement', '0008_remove_property_paid_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='owner_name',
        ),
    ]
