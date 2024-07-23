from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Colaborador, Departamento
from .models import Avaliacao, Pergunta, Resposta, Topico

class ColaboradorForm(UserCreationForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())
    cargo = forms.CharField(max_length=100)

    class Meta:
        model = Colaborador
        fields = ('nome', 'username', 'password1', 'password2', 'departamento', 'cargo', 'is_lider', 'is_coordenador', 'turno')



# class AvaliacaoForm(forms.ModelForm):
#     pontos_melhoria = forms.CharField(
#         widget=forms.Textarea, 
#         label='PONTOS DE MELHORIA (Para preenchimento juntamente com o líder)', 
#         required=False
#     )
#     pdi = forms.CharField(
#         widget=forms.Textarea, 
#         label='PDI - PLANO DE DESENVOLVIMENTO INDIVIDUAL (Para preenchimento juntamente com o líder)', 
#         required=False
#     )
#     metas = forms.CharField(
#         widget=forms.Textarea, 
#         label='METAS (Para preenchimento juntamente com o líder)', 
#         required=False
#     )
#     alinhamento = forms.CharField(
#         widget=forms.Textarea, 
#         label='ALINHAMENTO SEMESTRAL (Considerações)', 
#         required=False
#     )

#     class Meta:
#         model = Avaliacao
#         fields = [
#         'colaborador_avaliado', 'avaliador', 
#         ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['colaborador_avaliado'] = forms.ModelChoiceField(
#             queryset=Colaborador.objects.all(), 
#             label='Nome Completo'
#         )
#         self.fields['avaliador'] = forms.ModelChoiceField(
#             queryset=Colaborador.objects.filter(is_lider=True), 
#             label='Avaliador'
#         )

#         # Obtenha todos os tópicos e perguntas
#         topicos = Topico.objects.all()

#         # Itere sobre os tópicos
#         for topico in topicos:
#             # Adicione um campo para o tópico
#             self.fields[f'topico_{topico.id}'] = forms.CharField(
#                 label=topico.nome,
#                 widget=forms.TextInput(attrs={
#                     'readonly': 'readonly',
#                     'style': 'font-weight: bold; background-color: #f0f0f0; padding: 10px;'
#                 }),
#                 required=False
#             )

#             # Obtenha as perguntas associadas ao tópico
#             perguntas = topico.perguntas.all()

#             # Itere sobre as perguntas do tópico
#             for pergunta in perguntas:
#                 self.fields[f'pergunta_{pergunta.id}'] = forms.IntegerField(
#                     label=pergunta.texto,
#                     min_value=0,
#                     max_value=10,
#                     widget=forms.NumberInput(attrs={
#                         'placeholder': 'Digite uma nota de 0 a 10',
#                         'min': 0,
#                         'max': 10,
#                         'style': 'margin-left: 20px;'  # Adicione um recuo para as perguntas
#                     }),
#                     required=True
#                 )

#             # Adicione um campo de separação após cada tópico
#             self.fields[f'separator_{topico.id}'] = forms.CharField(
#                 label='',
#                 widget=forms.TextInput(attrs={
#                     'readonly': 'readonly',
#                     'style': 'border-bottom: 1px solid #ccc; display: block; margin-top: 10px;'
#                 }),
#                 required=False
#             )

#     def save(self, commit=True):
#         avaliacao = super().save(commit=False)  # Salva a instância de Avaliacao sem persistir no banco
#         if commit:
#             avaliacao.save()  # Salva a avaliação no banco de dados

#             # Salva as respostas das perguntas
#             for pergunta in Pergunta.objects.all():
#                 nota = self.cleaned_data.get(f'pergunta_{pergunta.id}')
#                 if nota is not None:  # Verifica se a nota foi preenchida
#                     Resposta.objects.create(avaliacao=avaliacao, pergunta=pergunta.id, nota=nota)

#         return avaliacao  # Retorna a instância de Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['colaborador_avaliado', 'avaliador', 'pontos_melhoria', 'pdi', 'metas', 'alinhamento_semestral', 'comentarios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colaborador_avaliado'] = forms.ModelChoiceField(
            queryset=Colaborador.objects.all(), 
            label='Nome Completo',
            required=True
        )
        self.fields['avaliador'] = forms.ModelChoiceField(
            queryset=Colaborador.objects.filter(is_lider=True), 
            label='Avaliador',
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
                required=True  # Torna o campo obrigatório
            )

    def save(self, commit=True):
        # Cria a avaliação sem salvar ainda
        avaliacao = super().save(commit=False)

        # Salva a avaliação no banco de dados
        if commit:
            avaliacao.save()  # Salva a avaliação

            # Salva as respostas relacionadas
            for pergunta in Pergunta.objects.all():
                resposta = self.cleaned_data.get(f'pergunta_{pergunta.id}')
                if resposta is not None:
                    Resposta.objects.create(avaliacao=avaliacao, pergunta=pergunta, nota=resposta)

        return avaliacao