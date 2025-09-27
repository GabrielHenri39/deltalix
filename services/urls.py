from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('protocolo/<str:protocolo>/', views.protocolo, name='mes_servico'),
    path('consulta/', views.consulta_servico, name='consulta_servico'),
    path('cancelar_servico/<str:protocolo>/', views.cancelar_servico, name='cancelar_servico'),
    path('cancelar_servico_confirmacao/<str:token>/', views.cancelar_servico_confirmacao, name='cancelar_servico_confirmacao'),
    ]