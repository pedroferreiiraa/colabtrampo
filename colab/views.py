from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.contrib import messages

from .forms import ColaboradorForm, AvaliacaoForm
from .models import Avaliacao

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f'Attempting login for username: {username}')  # Adicionando log
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador = form.save()  # Salva o colaborador
            messages.success(request, 'Cadastro realizado com sucesso! Você pode fazer login agora.')
            return redirect('login')
    else:
        form = ColaboradorForm()
    return render(request, 'cadastro.html', {'form': form})

def home_view(request):
    colaborador = request.user  # O usuário logado
    return render(request, 'home.html', {'colaborador': colaborador})


@login_required
def avaliacao_view(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a avaliação no banco de dados
            return redirect('home')  # Redirecionar após salvar
        else:
            print(form.errors)  # Imprime os erros para depuração
    else:
        form = AvaliacaoForm()
    
    return render(request, 'avaliacao.html', {'form': form})

@login_required
def avaliacao_logistica_view(request):
    lider = request.user
    avaliacoes = Avaliacao.objects.filter(
        colaborador_avaliado__departamento=lider.departamento
    )
    return render(request, 'avaliacao_logistica.html', {'avaliacoes': avaliacoes})

def avaliacao_detalhes(request, avaliacao_id):
    # Obtém a avaliação pelo ID ou retorna 404 se não existir
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    return render(request, 'avaliacao_detalhes.html', {'avaliacao': avaliacao})

def avaliacoes_list(request):
    # Supondo que você tenha um campo que identifica o líder
    lider = request.user  # Ou outra lógica para obter o líder
    avaliacoes = Avaliacao.objects.filter(avaliador=lider)  # Filtra avaliações feitas pelo líder

    return render(request, 'avaliacoes_list.html', {'avaliacoes': avaliacoes})