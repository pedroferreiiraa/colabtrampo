from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

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
            form.save()  # Salva a avaliação no banco de dados
            return redirect('home')  # Redirecionar após salvar
        else:
            print(form.errors)  # Imprime os erros para depuração
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

def salvar_avaliacao(request):
    if request.method == 'POST':
        # Crie uma nova instância de Avaliacao
        avaliacao = Avaliacao(
            colaborador_avaliado_id=request.POST.get('colaborador_avaliado'),
            avaliador_id=request.POST.get('avaliador'),
            data_avaliacao=request.POST.get('data_avaliacao'),
            pontos_melhoria=request.POST.get('pontos_melhoria'),
            pdi=request.POST.get('pdi'),
            metas=request.POST.get('metas'),
            alinhamento_semestral=request.POST.get('alinhamento_semestral'),
        )
        avaliacao.save()  # Salva a avaliação no banco de dados

        # Salvar as respostas
        for pergunta_id in request.POST.getlist('pergunta'):  # Supondo que você tenha um campo que lista as perguntas
            nota = request.POST.get(f'nota_{pergunta_id}')  # O nome do campo para a nota deve ser algo como 'nota_1', 'nota_2', etc.
            if nota:
                Resposta.objects.create(avaliacao=avaliacao, pergunta_id=pergunta_id, nota=nota)

        return redirect('')  # Redirecione para uma página de sucesso

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

# def avaliacao_detalhes(request, id):
#     avaliacao = get_object_or_404(Avaliacao, id)

#     # Crie um dicionário para armazenar perguntas e respostas
#     perguntas_respostas = {}
#     for i in range(1, 28):  # Supondo que você tenha 27 perguntas
#         pergunta = getattr(avaliacao, f'pergunta_{i}', None)
#         resposta = getattr(avaliacao, f'resposta_{i}', None)
#         if pergunta and resposta:
#             perguntas_respostas[pergunta] = resposta

#     return render(request, 'avaliacao_detalhes.html', {
#         'avaliacao': avaliacao,
#         'perguntas_respostas': perguntas_respostas,
#     })


def avaliacoes_list(request):
    avaliacoes = Avaliacao.objects.all()
    print(avaliacoes)
    return render(request, 'avaliacoes_list.html', {'avaliacoes': avaliacoes})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirecione para a página de login ou home