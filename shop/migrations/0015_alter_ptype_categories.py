# Generated by Django 5.1 on 2024-09-20 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_brand_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptype',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='shop.categories'),
        ),
    ]
