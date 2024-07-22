from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

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
    colaborador_avaliado = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    avaliador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_realizadas')
    data_avaliacao = models.DateField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    # Campos para armazenar as respostas das perguntas
    pergunta_1 = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    pergunta_2 = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    # Adicione mais campos conforme necessário

    def calcular_media_por_topico(self):
        medias = {}
        for topico in Topico.objects.all():
            respostas_topico = [resposta for pergunta_id, resposta in self.respostas.items() if pergunta_id in topico.perguntas.values_list('id', flat=True)]
            if respostas_topico:
                medias[topico.nome] = sum(respostas_topico) / len(respostas_topico)
        return medias