# Generated by Django 5.1.1 on 2024-11-26 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insumos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.TextField(max_length=30)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('metodouso', models.TextField(blank=True, max_length=100, null=True)),
                ('contraindicaciones', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='contraindicaciones',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='metodouso',
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='apellidos',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='contrasena',
            field=models.TextField(max_length=20),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='nombres',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='rut',
            field=models.TextField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='telefono',
            field=models.TextField(max_length=12),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.insumos'),
        ),
        migrations.CreateModel(
            name='InventarioOmnicell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.insumos')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.trabajador')),
            ],
        ),
    ]
