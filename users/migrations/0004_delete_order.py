# Generated by Django 3.1.2 on 2021-08-28 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
