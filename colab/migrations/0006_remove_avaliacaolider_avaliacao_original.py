# Generated by Django 5.0.7 on 2024-07-29 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colab', '0005_respostalider_colaborador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avaliacaolider',
            name='avaliacao_original',
        ),
    ]
