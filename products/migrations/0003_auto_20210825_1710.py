# Generated by Django 3.1.2 on 2021-08-25 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210825_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.IntegerField(default=True),
        ),
    ]
