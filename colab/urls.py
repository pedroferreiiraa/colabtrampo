from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
from .views import todas_avaliacoes, avaliacao_detalhes, logout_view, salvar_avaliacao,realizar_avaliacao, sucesso_view, avaliacao_lider,  todas_avaliacoes_rh, detalhes_avaliacao_rh, realizar_avaliacao_colaborador
urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home/', views.home_view, name='home'),

    #path('avaliacoes/', views.todas_avaliacoes, name='todas_avaliacoes'), # Isso aqui só ficará visível pro RH


    path('avaliacoes_rh/', views.todas_avaliacoes_rh, name='visualizar_avaliacoes_rh'),
    path('avaliacoes_rh/<int:avaliacao_id>/', views.detalhes_avaliacao_rh, name='detalhes_avaliacao_rh'),

    path('realizar_avaliacao/', realizar_avaliacao, name='realizar_avaliacao'),
    path('realizar_avaliacao_colaborador/<int:colaborador_id>/', realizar_avaliacao_colaborador, name='realizar_avaliacao_colaborador'),


    path('logout/', views.logout_view, name='logout'),
    path('salvar_avaliacao/', views.salvar_avaliacao, name='salvar_avaliacao'),

    path('sucesso/', views.sucesso_view, name='sucesso'),
   # path('avaliar/<int:avaliacao_id>/', avaliacao_lider, name='avaliacao_lider'),

]