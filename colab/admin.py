from django.contrib import admin
from .models import Topico, Pergunta, Colaborador, Departamento, Avaliacao, Turno, Resposta, AvaliacaoLider, AvaliacaoPerguntaResposta, RespostaLider
# Register your models here.

admin.site.register(Topico)
admin.site.register(Pergunta)
admin.site.register(Colaborador)
admin.site.register(Departamento)
admin.site.register(Avaliacao)
admin.site.register(Turno)
admin.site.register(Resposta)
admin.site.register(AvaliacaoLider)
admin.site.register(AvaliacaoPerguntaResposta)
admin.site.register(RespostaLider)