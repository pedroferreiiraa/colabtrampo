# Generated by Django 5.0.7 on 2024-07-30 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colab', '0008_avaliacao_avaliador_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avaliacao',
            name='avaliador_id',
        ),
        migrations.AddField(
            model_name='pergunta',
            name='competencias',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
