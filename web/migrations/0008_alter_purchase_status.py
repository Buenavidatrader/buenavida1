# Generated by Django 5.1.6 on 2025-03-26 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_purchase_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('entregado', 'Entregado')], default='pendiente', max_length=20),
        ),
    ]
