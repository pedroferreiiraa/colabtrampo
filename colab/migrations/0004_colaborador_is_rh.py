# Generated by Django 5.0.7 on 2024-07-26 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colab', '0003_alter_colaborador_funcao'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='is_rh',
            field=models.BooleanField(default=False),
        ),
    ]
