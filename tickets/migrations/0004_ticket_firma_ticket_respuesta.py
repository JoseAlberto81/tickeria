# Generated by Django 5.2.1 on 2025-05-28 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_rename_nombre_ticket_solicitante_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='firma',
            field=models.ImageField(blank=True, null=True, upload_to='firmas/'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='respuesta',
            field=models.TextField(blank=True, null=True),
        ),
    ]
