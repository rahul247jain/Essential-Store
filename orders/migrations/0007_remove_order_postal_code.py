# Generated by Django 2.2.8 on 2020-06-28 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200628_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='postal_code',
        ),
    ]
