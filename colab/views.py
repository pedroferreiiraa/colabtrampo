from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from django.db.models import Prefetch
from .forms import ColaboradorForm, AvaliacaoForm, Pergunta, AvaliacaoLiderForm, AvaliacaoLider
from .models import Avaliacao, Resposta, Colaborador, Departamento, RespostaLider

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

@login_required
def home_view(request):
    user = request.user

    # Obter avaliações realizadas pelo usuário
    avaliacoes_realizadas = Avaliacao.objects.filter(avaliador=user)

    # Obter avaliações recebidas pelo usuário
    avaliacoes_recebidas = Avaliacao.objects.filter(colaborador_avaliado=user)

    # Se o usuário for líder, obter avaliações do seu setor e turno
    avaliacoes_setor = None
    colaboradores_setor = None
    if user.is_lider:
        avaliacoes_setor = Avaliacao.objects.filter(
            colaborador_avaliado__departamento=user.departamento,
            colaborador_avaliado__turno=user.turno
        ).distinct()
        # Filtra os colaboradores do mesmo setor que não são líderes
        colaboradores_setor = Colaborador.objects.filter(departamento=user.departamento, is_lider=False)

    return render(request, 'home.html', {
        'avaliacoes_realizadas': avaliacoes_realizadas,
        'avaliacoes_recebidas': avaliacoes_recebidas,
        'avaliacoes_setor': avaliacoes_setor,
        'colaboradores_setor': colaboradores_setor,
        'is_lider': user.is_lider
    })

@login_required
def realizar_avaliacao(request):
    perguntas = Pergunta.objects.all()

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, user=request.user)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.avaliador = form.cleaned_data['avaliador']
            avaliacao.save()
            
            for pergunta in perguntas:
                resposta = form.cleaned_data.get(f'pergunta_{pergunta.id}')
                if resposta is not None:
                    Resposta.objects.create(
                        avaliacao=avaliacao,
                        pergunta=pergunta,
                        nota=resposta,
                        usuario=request.user
                    )
            
            return redirect('sucesso')
    else:
        form = AvaliacaoForm(user=request.user)
    
    return render(request, 'avaliacao.html', {
        'form': form,
        'perguntas': perguntas,
        'colaboradores': Colaborador.objects.all(),
        'avaliadores': Colaborador.objects.filter(is_lider=True),
    })


@login_required
def realizar_avaliacao_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    perguntas = Pergunta.objects.all()
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, user=request.user)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.colaborador_avaliado = colaborador
            avaliacao.avaliador = form.cleaned_data['avaliador']
            avaliacao.save()
            
            for pergunta in perguntas:
                resposta = form.cleaned_data.get(f'pergunta_{pergunta.id}')
                if resposta is not None:
                    Resposta.objects.create(
                        avaliacao=avaliacao,
                        pergunta=pergunta,
                        nota=resposta,
                        usuario=request.user
                    )
            
            return redirect('sucesso')
    else:
        initial_data = {
            'colaborador_avaliado': colaborador
        }
        form = AvaliacaoForm(user=request.user, initial=initial_data)
    
    return render(request, 'avaliacao.html', {
        'form': form,
        'perguntas': perguntas,
        'colaboradores': Colaborador.objects.all(),
        'avaliadores': Colaborador.objects.filter(is_lider=True),
    })



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
    # Obtém a avaliação específica
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    
    # Obtém as respostas do colaborador e do líder
    respostas_colaborador = Resposta.objects.filter(avaliacao=avaliacao, user=avaliacao.colaborador_avaliado)
    respostas_lider = Resposta.objects.filter(avaliacao=avaliacao, user=avaliacao.avaliador)
    
    # Calcula médias, se necessário
    media_colaborador = calcular_media(respostas_colaborador)
    media_lider = calcular_media(respostas_lider)
    
    return render(request, 'detalhes_avaliacao.html', {
        'avaliacao': avaliacao,
        'respostas_colaborador': respostas_colaborador,
        'respostas_lider': respostas_lider,
        'media_colaborador': media_colaborador,
        'media_lider': media_lider,
    })



@login_required
def todas_avaliacoes(request):
    # Verificar se o usuário é um líder
    if not request.user.is_lider:
        raise PermissionDenied("Você não tem permissão para acessar esta página.")

    # Filtrar as avaliações pelo departamento e turno do líder
    departamento = request.user.departamento
    turno = request.user.turno
    avaliacoes = Avaliacao.objects.filter(
        colaborador_avaliado__departamento=departamento,
        colaborador_avaliado__turno=turno
    )

    return render(request, 'avaliacoes_list.html', {'avaliacoes': avaliacoes})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirecione para a página de login ou home

def sucesso_view(request):
    return render(request, 'sucesso.html')  # Crie um template chamado sucesso.html

@login_required
def avaliacao_lider(request, avaliacao_id):
    # Obtém a avaliação original
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    
    # Verifica se o usuário é um líder e se a avaliação já não foi avaliada por esse líder
    if not request.user.is_lider or AvaliacaoLider.objects.filter(avaliacao_original=avaliacao, avaliador=request.user).exists():
        return redirect('home')  # Redireciona para a página inicial ou página de erro

    if request.method == 'POST':
        form = AvaliacaoLiderForm(request.POST)
        if form.is_valid():
            avaliacao_lider = form.save(commit=False)
            avaliacao_lider.avaliacao_original = avaliacao
            avaliacao_lider.avaliador = request.user
            avaliacao_lider.colaborador_avaliado = avaliacao.colaborador_avaliado
            avaliacao_lider.save()
            return redirect('home')  # Redireciona após salvar a avaliação
    else:
        form = AvaliacaoLiderForm()
    
    return render(request, 'avaliacao_lider.html', {'form': form, 'avaliacao': avaliacao})

@login_required
def todas_avaliacoes_rh(request):
    # Obtém todas as avaliações
    avaliacoes = Avaliacao.objects.all()

    # Agrupa as avaliações por departamento e turno
    avaliacoes_por_departamento = {}
    for avaliacao in avaliacoes:
        departamento = avaliacao.colaborador_avaliado.departamento  # Supondo que 'departamento' representa o departamento
        turno = avaliacao.colaborador_avaliado.turno  # Supondo que 'turno' representa o turno
        
        if departamento not in avaliacoes_por_departamento:
            avaliacoes_por_departamento[departamento] = {}
        
        if turno not in avaliacoes_por_departamento[departamento]:
            avaliacoes_por_departamento[departamento][turno] = []
        
        avaliacoes_por_departamento[departamento][turno].append(avaliacao)

    return render(request, 'visualizar_avaliacoes_rh.html', {
        'avaliacoes_por_departamento': avaliacoes_por_departamento,
    })

# @login_required
# def detalhes_avaliacao_rh(request, avaliacao_id):
#     avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    
#     # Obter todas as perguntas e tópicos
#     perguntas = Pergunta.objects.all()
#     topicos = Pergunta.objects.all()
#     respostas_colaborador = Resposta.objects.filter(avaliacao=avaliacao, usuario=avaliacao.colaborador_avaliado_id)
#     respostas_lider = Resposta.objects.filter(avaliacao=avaliacao, usuario=avaliacao.avaliador_id)
    
#     # Organizar respostas por tópico
#     respostas_por_topico = {topico.texto: {'colaborador': [], 'lider': [], 'media_colaborador': None, 'media_lider': None} for topico in topicos}
    
#     for resposta in respostas_colaborador:
#         respostas_por_topico[resposta.pergunta.topico.nome]['colaborador'].append(resposta)
    
#     for resposta in respostas_lider:
#         respostas_por_topico[resposta.pergunta.topico.nome]['lider'].append(resposta)
    
#     # Calcular médias por tópico
#     for topico, dados in respostas_por_topico.items():
#         dados['media_colaborador'] = calcular_media(dados['colaborador'])
#         dados['media_lider'] = calcular_media(dados['lider'])

#     return render(request, 'avaliacao_detalhes.html', {
#         'avaliacao': avaliacao,
#         'respostas_por_topico': respostas_por_topico,
#     })

def calcular_media(notas):
    if notas:
        # Assuming notas is a queryset of Resposta objects with a 'nota' field
        total = sum(resposta.nota for resposta in notas)  # Sum all the 'nota' values
        return total / len(notas)
    return None

@login_required
def detalhes_avaliacao_rh(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    
    perguntas = Pergunta.objects.all()
    respostas_por_topico = {}
    
    # Obter todas as respostas do colaborador associadas à avaliação
    respostas_colaborador = Resposta.objects.filter(avaliacao=avaliacao, usuario=avaliacao.colaborador_avaliado)
    respostas_lider = RespostaLider.objects.filter(avaliacao__avaliacao_original=avaliacao, colaborador=avaliacao.colaborador_avaliado)
    
    for pergunta in perguntas:
        topico_nome = pergunta.topico.nome
        if topico_nome not in respostas_por_topico:
            respostas_por_topico[topico_nome] = {
                'pares_colaborador': [],
                'pares_lider': [],
                'media_colaborador': None,
                'media_lider': None
            }
        
        respostas_por_topico[topico_nome]['pares_colaborador'].extend(
            [resposta for resposta in respostas_colaborador if resposta.pergunta == pergunta]
        )
        
        respostas_por_topico[topico_nome]['pares_lider'].extend(
            [resposta for resposta in respostas_lider if resposta.pergunta == pergunta]
        )
    
    # Calcular médias por tópico
    for topico, dados in respostas_por_topico.items():
        dados['media_colaborador'] = calcular_media(dados['pares_colaborador'])
        dados['media_lider'] = calcular_media(dados['pares_lider'])
    
    return render(request, 'detalhes_avaliacao_rh.html', {
        'avaliacao': avaliacao,
        'respostas_por_topico': respostas_por_topico,
    })

@login_required
def avaliacoes_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    avaliacoes = Avaliacao.objects.filter(colaborador_avaliado__departamento=departamento)
    
    return render(request, 'avaliacoes_departamento.html', {
        'departamento': departamento,
        'avaliacoes': avaliacoes,
    })