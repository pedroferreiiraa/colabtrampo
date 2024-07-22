from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
from .views import avaliacoes_list, avaliacao_detalhes, avaliacao_view, logout_view, salvar_avaliacao

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('home/', views.home_view, name='home'),
    path('avaliacoes/', avaliacoes_list, name='avaliacoes_list'),
    path('avaliacao/<int:avaliacao_id>/', views.avaliacao_detalhes, name='avaliacao_detalhes'),
    path('avaliacao/', avaliacao_view, name='avaliacao'),
    path('logout/', logout_view, name='logout'),
    path('salvar_avaliacao/', salvar_avaliacao, name='salvar_avaliacao'),

]