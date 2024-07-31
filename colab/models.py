from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import date


class Colaborador(AbstractUser):
    nome = models.CharField(max_length=200, blank=True)
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, null=True, blank=True)
    funcao = models.CharField(max_length=200, blank=True)
    is_lider = models.BooleanField(default=False)
    is_coordenador = models.BooleanField(default=False)
    is_rh = models.BooleanField(default=False)
    turno = models.ForeignKey('Turno', on_delete=models.CASCADE, null=True, blank=True)
    data_admissao = models.DateField(blank=True, null=True)  # Altere para DateField para consistência com o modelo Avaliacao
    cargo_atual = models.CharField(max_length=100, blank=True, null=True)  # Adicione o campo cargo_atual aqui
    area = models.CharField(max_length=100, blank=True, null=True)  # Adicione o campo area aqui
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
        db_table = 'colaborador'
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

class Turno(models.Model):
    turno = models.CharField(max_length=10)

    class Meta:
        db_table = 'turno'
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    def __str__(self):
        return self.turno
    
class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    lider = models.OneToOneField(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name='departamento_liderado')
    coordenador = models.OneToOneField(Colaborador, on_delete=models.SET_NULL, null=True, blank=True, related_name='departamento_coordenado')

    class Meta:
        db_table = 'departamento'
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nome
    
class Topico(models.Model):
    nome = models.TextField(max_length=100)

    class Meta:
        db_table = 'topico'
        verbose_name = "Tópico"
        verbose_name_plural = "Tópicos"

    def __str__(self):
        return self.nome


class Pergunta(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.CharField(max_length=255)
    competencias = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'pergunta'
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return self.texto  
        
class Avaliacao(models.Model):
    colaborador_avaliado = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    avaliador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_realizadas', blank=True, null=True)  # Assumindo que você quer registrar quem fez a avaliação
    data_avaliacao = models.DateField(default=date.today)
    pontos_melhoria = models.TextField(blank=True)
    pdi = models.TextField(blank=True)
    metas = models.CharField(max_length=100)


    class Meta:
        db_table = 'avaliacao'
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def get_respostas(self):
        respostas = {}
        for resposta in self.respostas.all():
            respostas[resposta.pergunta.id] = resposta.nota
        return respostas
    
    def __str__(self):
        return f"Avaliação de {self.colaborador_avaliado.nome}"
    
class Resposta(models.Model):
    usuario = models.ForeignKey(Colaborador, on_delete=models.CASCADE)  # Adiciona o campo usuário
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='respostas')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    nota = models.IntegerField()


    class Meta:
        db_table = 'resposta'
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
   

class AvaliacaoLider(models.Model):
    colaborador_avaliado = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_recebidas_lider')
    avaliador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='avaliacoes_realizadas_lider', blank=True, null=True)  # Assumindo que você quer registrar quem fez a avaliação
    data_avaliacao = models.DateField(default=date.today)
    competencias = models.CharField(max_length=100, null=True, blank=True)
    compromissos = models.CharField(max_length=100, null=True, blank=True)
    integracao = models.CharField(max_length=100, null=True, blank=True)
    caracteristicas = models.CharField(max_length=100, null=True, blank=True)
    pontos_melhoria = models.TextField(blank=True, null=True)
    pdi = models.TextField(blank=True, null=True)
    metas = models.CharField(max_length=100, null=True, blank=True)
    alinhamento_semestral = models.CharField(max_length=100, null=True, blank=True)
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'avaliacao_lider'
        verbose_name = "Avaliação do Líder"
        verbose_name_plural = "Avaliações dos Líderes"

    def get_respostas(self):
        respostas = {}
        for resposta in self.respostas_lider.all():
            respostas[resposta.pergunta.id] = resposta.nota
        return respostas
    
    def __str__(self):
        return f"Avaliação de {self.avaliador} para {self.colaborador_avaliado}"

class RespostaLider(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='respostas_lider', null=True, blank=True)  # Referência ao usuário
    avaliacao = models.ForeignKey(AvaliacaoLider, on_delete=models.CASCADE, related_name='respostas_lider')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    nota = models.IntegerField()
    texto = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'resposta_lider'
        verbose_name = "Resposta do Líder"
        verbose_name_plural = "Respostas dos Líderes"

class AvaliacaoPerguntaResposta(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    nota = models.IntegerField(blank=True, null=True)
    texto = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'avaliacao_pergunta_resposta'
        verbose_name = "Avaliação Pergunta Resposta"
        verbose_name_plural = "Avaliações Perguntas Respostas"