# Generated by Django 3.1.7 on 2021-02-25 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('descricao', models.TextField()),
                ('fornecedor', models.CharField(max_length=300)),
                ('quantidade_maxima', models.PositiveIntegerField()),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
