from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Colaborador, Departamento
from .models import Avaliacao, Pergunta, Resposta, AvaliacaoLider, RespostaLider

class ColaboradorForm(UserCreationForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())
    cargo = forms.CharField(max_length=100)

    class Meta:
        model = Colaborador
        fields = ('nome', 'username', 'password1', 'password2', 'departamento', 'cargo', 'is_lider', 'is_coordenador', 'turno')

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = [
            'colaborador_avaliado',
            'nome_completo', 'data_admissao', 'cargo_atual', 'avaliador', 
            'area', 'periodo_referencia', 'data_avaliacao',
            'competencias', 'compromissos', 'integracao', 'caracteristicas', 'pontos_melhoria', 
            'pdi', 'metas', 'alinhamento_semestral', 'comentarios'
        ]
        labels = {
            'colaborador_avaliado': 'Colaborador avaliado',
            'nome_completo': 'Nome Completo',
            'data_admissao': 'Data / Admissão',
            'cargo_atual': 'Cargo Atual',
            'avaliador': 'Avaliador',
            'area': 'Área',
            'periodo_referencia': 'Período de Referência',
            'data_inicial': 'Data Inicial',
            'data_final': 'Data Final',
            'data_avaliacao': 'Data Avaliação',
            'competencias': 'Competências/Habilidades',
            'compromissos': 'Compromisso com Resultados',
            'integracao': 'Integração Institucional',
            'caracteristicas': 'Características Comportamentais',
            'pontos_melhoria': 'Pontos de Melhoria',
            'pdi': 'PDI - Plano de Desenvolvimento Individual',
            'metas': 'Metas',
            'alinhamento_semestral': 'Alinhamento Semestral',
            'comentarios': 'Comentários Adicionais'
        }
        widgets = {
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
            'data_cargo': forms.DateInput(attrs={'type': 'date'}),
            'data_inicial': forms.DateInput(attrs={'type': 'date'}),
            'data_final': forms.DateInput(attrs={'type': 'date'}),
            'data_avaliacao': forms.DateInput(attrs={'type': 'date'}),
            'competencias': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'compromissos': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'integracao': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'caracteristicas': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'pontos_melhoria': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'pdi': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'metas': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'alinhamento_semestral': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'comentarios': forms.Textarea(attrs={'rows': 4, 'cols': 15})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super(AvaliacaoForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['nome_completo'].initial = user.get_full_name()

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'style': 'border: 1px solid #ced4da; border-radius: .25rem; padding: .375rem .75rem; display: block'
            })
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
                    'max': 10,
                    'class': 'form-control',
                    'style': 'border: 1px solid #ced4da; border-radius: .25rem; padding: .375rem .75rem;'
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

class AvaliacaoLiderForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoLider
        fields = ['avaliacao_original', 'colaborador_avaliado', 'avaliador', 'pontos_melhoria', 'pdi', 'metas', 'alinhamento_semestral', 'comentarios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avaliacao_original'] = forms.ModelChoiceField(
            queryset=Avaliacao.objects.all(),
            label='Avaliação Original',
            required=True
        )
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