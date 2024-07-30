from django.urls import path

from . import views
from .views import todas_avaliacoes, avaliacao_detalhes, logout_view,  sucesso_view, avaliacao_lider,  todas_avaliacoes_rh, detalhes_avaliacao_rh, realizar_avaliacao_colaborador, realizar_avaliacao_lider, salvar_avaliacao_colaborador, salvar_avaliacao_lider, detalhes_avaliacao_lider
urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home/', views.home_view, name='home'),
    path('home/<int:departamento_id>/', views.listar_colaboradores, name='listar_colaboradores'),

    path('logout/', views.logout_view, name='logout'),

    path('avaliacoes_rh/', views.todas_avaliacoes_rh, name='visualizar_avaliacoes_rh'),
    path('avaliacoes_rh/<int:avaliacao_id>/', views.detalhes_avaliacao_rh, name='detalhes_avaliacao_rh'),
    path('avaliacoes_rh/departamento/<int:departamento_id>/', views.avaliacoes_departamento, name='avaliacoes_departamento'),

    path('detalhes_avaliacao_lider/<int:avaliacao_lider_id>/', views.detalhes_avaliacao_lider, name='detalhes_avaliacao_lider'),

    path('departamentos/', views.listar_departamentos, name='listar_departamentos'),
    path('departamentos/<int:departamento_id>/colaboradores/', views.listar_colaboradores, name='listar_colaboradores'),


    path('colaboradores/<int:colaborador_id>/avaliacoes/', views.listar_avaliacoes_colaborador, name='listar_avaliacoes_colaborador'),
    path('colaboradores/<int:colaborador_id>/avaliacoes_lider/', views.listar_avaliacoes_lider, name='listar_avaliacoes_lider'),
    
    path('avaliacoes/<int:id>/', views.detalhes_avaliacao, name='detalhes_avaliacao'),

    path('realizar_avaliacao_colaborador/', views.realizar_avaliacao_colaborador, name='realizar_avaliacao_colaborador'),
    #path('realizar_avaliacao_colaborador/<int:colaborador_id>/', realizar_avaliacao_colaborador, name='realizar_avaliacao_colaborador'),
    path('realizar_avaliacao_lider/<int:colaborador_id>/', realizar_avaliacao_lider, name='realizar_avaliacao_lider'),


    path('salvar_avaliacao_colaborador/', views.salvar_avaliacao_colaborador, name='salvar_avaliacao_colaborador'),
    path('salvar_avaliacao_lider/<int:colaborador_id>/', salvar_avaliacao_lider, name='salvar_avaliacao_lider'),

    path('sucesso/', views.sucesso_view, name='sucesso'),
   # path('avaliar/<int:avaliacao_id>/', avaliacao_lider, name='avaliacao_lider'),

]