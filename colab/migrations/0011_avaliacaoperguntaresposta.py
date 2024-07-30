# Generated by Django 5.0.7 on 2024-07-30 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colab', '0010_remove_avaliacao_area_remove_avaliacao_cargo_atual_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvaliacaoPerguntaResposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(blank=True, null=True)),
                ('texto', models.TextField(blank=True, null=True)),
                ('avaliacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacao_perguntas', to='colab.avaliacao')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colab.pergunta')),
            ],
            options={
                'unique_together': {('avaliacao', 'pergunta')},
            },
        ),
    ]
