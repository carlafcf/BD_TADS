# Generated by Django 3.1.7 on 2021-03-04 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Produto', '0002_auto_20210225_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='data_validade',
        ),
    ]
