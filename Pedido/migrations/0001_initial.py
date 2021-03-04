# Generated by Django 3.1.7 on 2021-03-04 18:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=datetime.date.today)),
                ('status', models.CharField(choices=[('1', 'Em espera'), ('2', 'Cadastrado'), ('3', 'Em análise'), ('4', 'Esperando chegar'), ('5', 'Finalizado')], default='1', max_length=1)),
            ],
            options={
                'ordering': ['data', 'status'],
            },
        ),
    ]
