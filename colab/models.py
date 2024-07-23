from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class Colaborador(AbstractUser):
    nome = models.CharField(max_length=200, blank=True)
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

    class Meta:
        db_table = 'colaborador'  # Use letras minúsculas para nomes de tabelas

class Turno(models.Model):
    turno = models.CharField(max_length=10)    

    class Meta:
        db_table = 'turno'

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    lider = models.OneToOneField(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name='departamento_liderado')
    coordenador = models.OneToOneField(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name='departamento_coordenado')

    class Meta:
        db_table = 'departamento'
    
class Topico(models.Model):
    nome = models.TextField(max_length=100)

    class Meta:
        db_table = 'topico'

    def __str__(self):
        return self.nome


class Pergunta(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.CharField(max_length=255)

    class Meta:
        db_table = 'pergunta'

    def __str__(self):
        return self.texto    
    

    
class Avaliacao(models.Model):
    colaborador_avaliado = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    avaliador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_realizadas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    pontos_melhoria = models.TextField(null=True, blank=True)
    pdi = models.TextField(null=True, blank=True)
    metas = models.TextField(null=True, blank=True)
    alinhamento_semestral = models.TextField(null=True, blank=True)
    media_geral = models.FloatField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'avaliacao'

    def get_respostas(self):
        respostas = {}
        for resposta in self.respostas.all():  # Acessa todas as respostas relacionadas
            respostas[resposta.pergunta.id] = resposta.nota  # Usa o ID da pergunta como chave
        return respostas
    
class Resposta(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    nota = models.IntegerField()

    class Meta:
        db_table = 'resposta'
