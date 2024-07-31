from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Colaborador, Departamento
from .models import Avaliacao, Pergunta, Resposta, AvaliacaoLider, RespostaLider, AvaliacaoPerguntaResposta

class ColaboradorForm(UserCreationForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())    
    data_admissao = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'})
    )

    class Meta:
        model = Colaborador
        
        fields = ('nome', 'username', 'password1', 'password2', 'departamento', 'turno', 'data_admissao', 'funcao', 'is_lider', 'is_coordenador', 'is_rh')
        labels = {
            'username': 'Usuário',
            'password1': 'Senha',
            'password2': 'Senha'
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = [
            'colaborador_avaliado', 'avaliador', 'data_avaliacao', 
            'pontos_melhoria', 'pdi', 'metas', 
        ]
        labels = {
            'colaborador_avaliado': 'Colaborador avaliado',
            'avaliador': 'Avaliador',
            'data_avaliacao': 'Data Avaliação',
            'pontos_melhoria': 'Pontos de Melhoria',
            'pdi': 'PDI - Plano de Desenvolvimento Individual',
            'metas': 'Metas',
        }
        widgets = {
            'data_avaliacao': forms.DateInput(attrs={'type': 'date'}),
            'pontos_melhoria': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'pdi': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'metas': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AvaliacaoForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['colaborador_avaliado'].initial = self.user
            self.fields['avaliador'].initial = self.user

        # Adiciona atributos de estilo a todos os campos
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'style': 'border: 1px solid #ced4da; border-radius: .25rem; padding: .375rem .75rem; display: block'
            })
        
        # Agrupando perguntas por tópico
        perguntas = Pergunta.objects.all().select_related('topico')
        topicos_perguntas = {}
        
        for pergunta in perguntas:
            if pergunta.topico not in topicos_perguntas:
                topicos_perguntas[pergunta.topico] = []
            topicos_perguntas[pergunta.topico].append(pergunta)

            # Campo para nota
            self.fields[f'pergunta_{pergunta.id}_nota'] = forms.IntegerField(
                label=pergunta.texto,
                min_value=0,
                max_value=10,
                widget=forms.NumberInput(attrs={
                    'placeholder': 'Digite uma nota de 0 a 10',
                    'min': 0,
                    'max': 10,
                    'class': 'form-control',
                    'style': 'border: 1px solid #ced4da; border-radius: .25rem; padding: .375rem .75rem;'
                }),
                required=True
            )

            # Campo para competências
            self.fields[f'pergunta_{pergunta.id}_competencias'] = forms.CharField(
                label=f'Competência: {pergunta.competencias}',
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'style': 'border: 1px solid #ced4da; border-radius: .25rem; padding: .375rem .75rem;'
                }),
                required=False
            )

        # Armazenar os tópicos e suas perguntas para uso no template
        self.topicos_perguntas = topicos_perguntas

        def save(self, commit=True):
            # Cria a avaliação sem salvar ainda
            avaliacao = super().save(commit=False)

            # Salva a avaliação no banco de dados
            if commit:
                avaliacao.save()

                # Salva as respostas relacionadas
                for pergunta in Pergunta.objects.all():
                    # Obtém a nota e a competência do formulário
                    nota = self.cleaned_data.get(f'pergunta_{pergunta.id}_nota')
                    competencias = self.cleaned_data.get(f'pergunta_{pergunta.id}_competencias')

                    if nota is not None:  # Verifica se a nota foi fornecida
                        Resposta.objects.create(
                            avaliacao=avaliacao,
                            pergunta=pergunta,
                            nota=nota,
                            usuario=self.user
                        )
                        
            return avaliacao

# class AvaliacaoForm(forms.ModelForm):
#     class Meta:
#         model = Avaliacao
#         fields = [
#             'colaborador_avaliado', 'data_avaliacao',
#             'competencias', 'compromissos', 'integracao', 'caracteristicas', 'pontos_melhoria', 
#             'pdi', 'metas', 'alinhamento_semestral', 'comentarios'
#         ]
#         labels = {
#             'colaborador_avaliado': 'Colaborador avaliado',
#             'avaliador': 'Avaliador',
#             'data_avaliacao': 'Data Avaliação',
#             'competencias': 'Competências/Habilidades',
#             'compromissos': 'Compromisso com Resultados',
#             'integracao': 'Integração Institucional',
#             'caracteristicas': 'Características Comportamentais',
#             'pontos_melhoria': 'Pontos de Melhoria',
#             'pdi': 'PDI - Plano de Desenvolvimento Individual',
#             'metas': 'Metas',
#             'alinhamento_semestral': 'Alinhamento Semestral',
#             'comentarios': 'Comentários Adicionais' 
#         }
#         widgets = {
#             'data_avaliacao': forms.DateInput(attrs={'type': 'date'}),
#             'competencias': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'compromissos': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'integracao': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'caracteristicas': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'pontos_melhoria': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'pdi': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'metas': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'alinhamento_semestral': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
#             'comentarios': forms.Textarea(attrs={'rows': 4, 'cols': 15})
#         }

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(AvaliacaoForm, self).__init__(*args, **kwargs)

#         if self.user:
#             # Define o campo 'colaborador_avaliado' com o usuário atual
#             self.fields['colaborador_avaliado'].initial = self.user
#             # Define o campo 'nome_completo' com o nome do usuário atual
#             #self.fields['nome_completo'].initial = self.user.get_full_name()
#             # Filtra o campo 'avaliador' para exibir apenas os líderes

#         for field_name in self.fields:
#             self.fields[field_name].widget.attrs.update({
#                 'class': 'form-control',
#                 'style': 'border: 1px solid #ced4da; border-radius: .25rem; padding: .375rem .75rem; display: block'
#             })
#         # Adiciona perguntas dinamicamente

#         perguntas = Pergunta.objects.all().select_related('topico')
#         for pergunta in perguntas:
#             self.fields[f'pergunta_{pergunta.id}'] = forms.IntegerField(
#                 label=pergunta.texto,
#                 min_value=0,
#                 max_value=10,
#                 widget=forms.NumberInput(attrs={
#                     'placeholder': 'Digite uma nota de 0 a 10',
#                     'min': 0,
#                     'max': 10,
#                     'class': 'form-control',
#                     'style': 'border: 1px solid #ced4da; border-radius: .25rem; padding: .375rem .75rem;'
#                 }),
#                 required=True  # Torna o campo obrigatório
#             )

#     def save(self, commit=True):
#         # Cria a avaliação sem salvar ainda
#         avaliacao = super().save(commit=False)

#         # Salva a avaliação no banco de dados
#         if commit:
#             avaliacao.save()  # Salva a avaliação

#             # Salva as respostas relacionadas
#             for pergunta in Pergunta.objects.all():
#                 resposta = self.cleaned_data.get(f'pergunta_{pergunta.id}')
#                 if resposta is not None:
#                     Resposta.objects.create(
#                         avaliacao=avaliacao,
#                         pergunta=pergunta,
#                         nota=resposta,
#                         usuario=self.user  # Define o usuário
#                     )
                    
#         return avaliacao


class AvaliacaoLiderForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoLider
        fields = ['colaborador_avaliado','pontos_melhoria', 'pdi', 'metas', 'alinhamento_semestral', 'comentarios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colaborador_avaliado'] = forms.ModelChoiceField(
            queryset=Colaborador.objects.all(),
            label='Nome Completo',
            required=True
        )
        # Adiciona perguntas dinamicamente
        perguntas = Pergunta.objects.all()
        for pergunta in perguntas:
            self.fields[f'pergunta_{pergunta.id}'] = forms.IntegerField(
                label=pergunta.texto,
                min_value=0,
                max_value=10,
                widget=forms.NumberInput(attrs={
                    'placeholder': 'Digite uma nota de 0 a 10',
                    'min': 0,
                    'max': 10
                }),
                required=True
            )

    def save(self, commit=True):
        # Cria a avaliação do líder sem salvar ainda
        avaliacao = super().save(commit=False)

        # Salva a avaliação no banco de dados
        if commit:
            avaliacao.save()

            # Salva as respostas relacionadas
            for pergunta in Pergunta.objects.all():
                resposta = self.cleaned_data.get(f'pergunta_{pergunta.id}')
                if resposta is not None:
                    RespostaLider.objects.create(avaliacao=avaliacao, pergunta=pergunta, nota=resposta)

        return avaliacao