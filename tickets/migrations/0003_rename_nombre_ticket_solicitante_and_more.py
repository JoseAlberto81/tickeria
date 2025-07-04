# Generated by Django 5.2.1 on 2025-05-27 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_ticket_archivo_ticket_fecha_esperada_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='nombre',
            new_name='solicitante',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='asunto',
            new_name='titulo',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='archivo',
        ),
        migrations.AddField(
            model_name='ticket',
            name='asignado',
            field=models.CharField(blank=True, default='HelpDesk', max_length=100),
        ),
        migrations.AddField(
            model_name='ticket',
            name='etiqueta',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='estado',
            field=models.CharField(choices=[('Abierto', 'Abierto'), ('En progreso', 'En progreso'), ('Cerrado', 'Cerrado')], default='Abierto', max_length=20),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='prioridad',
            field=models.CharField(blank=True, choices=[('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Importante', 'Importante')], max_length=20),
        ),
    ]
