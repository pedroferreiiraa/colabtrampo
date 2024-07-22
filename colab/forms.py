from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Colaborador, Departamento
from .models import Avaliacao, Pergunta

class ColaboradorForm(UserCreationForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())
    cargo = forms.CharField(max_length=100)

    class Meta:
        model = Colaborador
        fields = ('username', 'password1', 'password2', 'departamento', 'cargo', 'is_lider', 'is_coordenador', 'turno')



class AvaliacaoForm(forms.ModelForm):
    pontos_melhoria = forms.CharField(widget=forms.Textarea, label='PONTOS DE MELHORIA (Para preenchimento juntamente com o líder)', required=False)
    pdi = forms.CharField(widget=forms.Textarea, label='PDI - PLANO DE DESENVOLVIMENTO INDIVIDUAL (Para preenchimento juntamente com o líder)', required=False)
    metas = forms.CharField(widget=forms.Textarea, label='METAS (Para preenchimento juntamente com o líder)', required=False)
    alinhamento = forms.CharField(widget=forms.Textarea, label='ALINHAMENTO SEMESTRAL (Considerações)', required=False)

    class Meta:
        model = Avaliacao
        fields = ['colaborador_avaliado', 'avaliador', 'data_avaliacao', 'pontos_melhoria', 'pdi', 'metas', 'alinhamento', 'pergunta_1', 'pergunta_2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colaborador_avaliado'] = forms.ModelChoiceField(queryset=Colaborador.objects.all(), label='Nome Completo')
        self.fields['avaliador'] = forms.ModelChoiceField(queryset=Colaborador.objects.filter(is_lider=True), label='Avaliador')
        self.fields['data_avaliacao'] = forms.DateField(label='Data Avaliação')

        # Adiciona perguntas dinamicamente
        perguntas = Pergunta.objects.all()
        for pergunta in perguntas:
            self.fields[f'pergunta_{pergunta.id}'] = forms.DecimalField(
                label=pergunta.texto,
                max_digits=2,
                decimal_places=1,
                min_value=1,
                max_value=10,
                widget=forms.NumberInput(attrs={'placeholder': 'Digite uma nota de 1 a 10'})
            )

    
    def save(self, commit=True):
        return super().save(commit=commit)