# Generated by Django 5.1.4 on 2024-12-18 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_dealer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
