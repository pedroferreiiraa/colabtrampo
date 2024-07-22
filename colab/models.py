from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django import forms

class Colaborador(AbstractUser):
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, null=True, blank=True)
    cargo = models.CharField(max_length=100)
    is_lider = models.BooleanField(default=False)
    is_coordenador = models.BooleanField(default=False)
    turno = models.ForeignKey('Turno', on_delete=models.CASCADE, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='colaboradores',
        blank=True,
        help_text='Grupos a que este usuário pertence.',
        verbose_name='Grupos'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='colaboradores',
        blank=True,
        help_text='Permissões específicas concedidas a este usuário.',
        verbose_name='Permissões'
    )

class Turno(models.Model):
    turno = models.CharField(max_length=10)    

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    lider = models.OneToOneField(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name='departamento_liderado')
    coordenador = models.OneToOneField(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name='departamento_coordenado')
    
class Topico(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Pergunta(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto

class Avaliacao(models.Model):
    colaborador_avaliado = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    avaliador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='avaliacoes_realizadas')
    data = models.DateTimeField(auto_now_add=True)
    pontos_melhoria = models.TextField(null=True, blank=True)
    pdi = models.TextField(null=True, blank=True)
    metas = models.TextField(null=True, blank=True)
    alinhamento_semestral = models.TextField(null=True, blank=True)


    def get_respostas(self):
        respostas = {}
        for resposta in self.respostas.all():  # Acessa todas as respostas relacionadas
            respostas[resposta.pergunta.id] = resposta.nota  # Usa o ID da pergunta como chave
        return respostas

class Resposta(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas')
    nota = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Resposta para {self.pergunta.texto}: {self.nota}'


# class Avaliacao(models.Model):
#     colaborador_avaliado = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
#     avaliador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_realizadas')
#     data_avaliacao = models.DateField(blank=True, null=True)
#     data = models.DateTimeField(auto_now_add=True)
#     pontos_melhoria = models.TextField(null=True, blank=True)
#     pdi = models.TextField(null=True, blank=True)
#     metas = models.TextField(null=True, blank=True)
#     alinhamento_semestral = models.TextField(null=True, blank=True)

#     pergunta_1 = models.IntegerField(   blank=True, null=True)
#     pergunta_2 = models.IntegerField(    blank=True, null=True)
#     pergunta_3 = models.IntegerField(    blank=True, null=True)
#     pergunta_4 = models.IntegerField(    blank=True, null=True)
#     pergunta_5 = models.IntegerField(    blank=True, null=True)
#     pergunta_6 = models.IntegerField(    blank=True, null=True)
#     pergunta_7 = models.IntegerField(    blank=True, null=True)
#     pergunta_8 = models.IntegerField(    blank=True, null=True)
#     pergunta_9 = models.IntegerField(    blank=True, null=True)
#     pergunta_10 = models.IntegerField(    blank=True, null=True)
#     pergunta_11 = models.IntegerField(    blank=True, null=True)
#     pergunta_12 = models.IntegerField(    blank=True, null=True)
#     pergunta_13 = models.IntegerField(    blank=True, null=True)
#     pergunta_14 = models.IntegerField(    blank=True, null=True)
#     pergunta_15 = models.IntegerField(    blank=True, null=True)
#     pergunta_16 = models.IntegerField(    blank=True, null=True)
#     pergunta_17 = models.IntegerField(    blank=True, null=True)
#     pergunta_18 = models.IntegerField(    blank=True, null=True)
#     pergunta_19 = models.IntegerField(    blank=True, null=True)
#     pergunta_20 = models.IntegerField(    blank=True, null=True)
#     pergunta_21 = models.IntegerField(    blank=True, null=True)
#     pergunta_22 = models.IntegerField(    blank=True, null=True)
#     pergunta_23 = models.IntegerField(    blank=True, null=True)
#     pergunta_24 = models.IntegerField(    blank=True, null=True)
#     pergunta_25 = models.IntegerField(    blank=True, null=True)
#     pergunta_26 = models.IntegerField(    blank=True, null=True)
#     pergunta_27 = models.IntegerField(    blank=True, null=True)
#     pergunta_28 = models.IntegerField(    blank=True, null=True)
#     pergunta_29 = models.IntegerField(    blank=True, null=True)
#     pergunta_30 = models.IntegerField(    blank=True, null=True)
#     pergunta_31 = models.IntegerField(    blank=True, null=True)
#     pergunta_32 = models.IntegerField(    blank=True, null=True)
#     pergunta_33 = models.IntegerField(    blank=True, null=True)
#     pergunta_34 = models.IntegerField(    blank=True, null=True)
#     pergunta_35 = models.IntegerField(    blank=True, null=True)
#     pergunta_36 = models.IntegerField(    blank=True, null=True)
#     pergunta_37 = models.IntegerField(    blank=True, null=True)

#     def get_respostas(self):
#         respostas = {}
#         for i in range(1, 37):  # Supondo que você tenha 36 perguntas
#             respostas[f'pergunta_{i}'] = getattr(self, f'pergunta_{i}', None)
#         return respostas
