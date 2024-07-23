from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.db.models import Q

from django.contrib import messages

from .forms import ColaboradorForm, AvaliacaoForm, Pergunta
from .models import Avaliacao, Resposta, Colaborador

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
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.save()
            form.save_m2m()  # Salva as relações many-to-many
            return redirect('home')
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliacao.html', {'form': form})


@login_required
def avaliacao(request):
    perguntas = Pergunta.objects.all()  # Obtém todas as perguntas
    return render(request, 'avaliacao_form.html', {
        'perguntas': perguntas,
        'colaboradores': Colaborador.objects.all(),  # Supondo que você tenha uma lista de colaboradores
        'avaliadores': Colaborador.objects.all(),  # Supondo que você tenha uma lista de avaliadores
    })

def realizar_avaliacao(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            # Cria a avaliação e salva no banco de dados
            avaliacao = form.save(commit=False)
            avaliacao.avaliador = request.user  # Define o avaliador como o usuário atual
            avaliacao.save()
            
            # Salva as respostas relacionadas
            for pergunta in Pergunta.objects.all():
                resposta = form.cleaned_data.get(f'pergunta_{pergunta.id}')
                if resposta is not None:
                    Resposta.objects.create(avaliacao=avaliacao, pergunta=pergunta, nota=resposta)
            
            return redirect('sucesso')  # Redireciona para uma página de sucesso
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliacao.html', {'form': form})

def salvar_avaliacao(request):
    if request.method == 'POST':
        # Crie uma nova instância de Avaliacao
        avaliacao = Avaliacao(
            colaborador_avaliado_id=request.POST.get('colaborador_avaliado'),
            avaliador_id=request.POST.get('avaliador'),
            pontos_melhoria=request.POST.get('pontos_melhoria'),
            pdi=request.POST.get('pdi'),
            metas=request.POST.get('metas'),
            alinhamento_semestral=request.POST.get('alinhamento_semestral'),
            # Se você tiver um campo de data de avaliação, descomente a linha abaixo
            # data_avaliacao=request.POST.get('data_avaliacao'),
        )
        avaliacao.save()  # Salva a avaliação no banco de dados

        # Salvar as respostas
        perguntas = Pergunta.objects.all()  # Obtém todas as perguntas
        for pergunta in perguntas:
            nota = request.POST.get(f'pergunta_{pergunta.id}')  # O nome do campo para a nota deve ser algo como 'pergunta_1', 'pergunta_2', etc.
            if nota:
                Resposta.objects.create(avaliacao=avaliacao, pergunta=pergunta, nota=nota)

        return redirect('sucesso')  # Redirecione para uma página de sucesso

    # Se não for um POST, renderize o formulário novamente
    return render(request, 'salvar_avaliacao.html')  # Renderize o formulário novamente em caso de erro
    

def avaliacao_detalhes(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)

    # Obter todas as perguntas
    perguntas = Pergunta.objects.all()
    respostas_por_topico = {}
    numeros_perguntas = list(range(1, 27))  # Ajuste o range para 1-38 devido à pergunta_37
    respostas = avaliacao.get_respostas()

    print(respostas)  # Adicione esta linha para verificar o conteúdo
    print(type(respostas))  # Isso deve imprimir <class 'dict'>

    # Verificar se o número de perguntas é suficiente
    total_perguntas = len(perguntas)

    for i in range(1, total_perguntas + 1):
        if i <= total_perguntas:  # Verifica se o índice está dentro do intervalo
            topico_nome = perguntas[i-1].topico.nome
            if topico_nome not in respostas_por_topico:
                respostas_por_topico[topico_nome] = {'notas': [], 'perguntas': []}
            nota = respostas.get(f'pergunta_{i}')  # Use o método get para evitar KeyError
            if nota is not None:  # Apenas adiciona notas que não são None
                respostas_por_topico[topico_nome]['notas'].append(nota)
                respostas_por_topico[topico_nome]['perguntas'].append(perguntas[i-1])

    # Calcular médias
    for topico, dados in respostas_por_topico.items():
        if dados['notas']:
            notas_validas = [nota for nota in dados['notas'] if nota is not None]
            if notas_validas:  # Verifica se há notas válidas
                media = sum(notas_validas) / len(notas_validas)
                dados['media'] = media
            else:
                dados['media'] = None
        else:
            dados['media'] = None

    return render(request, 'avaliacao_detalhes.html', {
        'avaliacao': avaliacao,
        'respostas_por_topico': respostas_por_topico,
        'respostas': respostas,  # Passa o dicionário de respostas para o template
        'numeros_perguntas': numeros_perguntas,
    })


def avaliacoes_list(request):
    # Busca todas as avaliações do banco de dados
    avaliacoes = Avaliacao.objects.all()
    return render(request, 'avaliacoes_list.html', {'avaliacoes': avaliacoes})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirecione para a página de login ou home

def sucesso_view(request):
    return render(request, 'sucesso.html')  # Crie um template chamado sucesso.html