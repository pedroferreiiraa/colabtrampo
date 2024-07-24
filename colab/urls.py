from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
from .views import avaliacoes_list, avaliacao_detalhes, avaliacao_view, logout_view, salvar_avaliacao,realizar_avaliacao, sucesso_view, avaliacao_lider, detalhes_avaliacao_rh, visualizar_avaliacoes_rh

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home/', views.home_view, name='home'),
    path('avaliacoes/', views.avaliacoes_list, name='avaliacoes_list'),
    #path('avaliacoes/', todas_avaliacoes_rh, name='todas_avaliacoes'),
    path('avaliacoes/<int:avaliacao_id>/', detalhes_avaliacao_rh, name='detalhes_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/', views.avaliacao_detalhes, name='avaliacao_detalhes'),
    path('avaliacao/', views.avaliacao_view, name='avaliacao'),
    path('logout/', views.logout_view, name='logout'),
    path('salvar_avaliacao/', views.salvar_avaliacao, name='salvar_avaliacao'),
    path('realizar_avaliacao/', views.realizar_avaliacao, name='realizar_avaliacao'),
    path('sucesso/', views.sucesso_view, name='sucesso'),
    path('avaliar/<int:avaliacao_id>/', avaliacao_lider, name='avaliacao_lider'),
    path('visualizar-avaliacoes-rh/', visualizar_avaliacoes_rh, name='visualizar_avaliacoes_rh'),
    
]