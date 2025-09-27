from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin/',views.admin_list_view,name='admin_list'),
    path('admin/servicos_json/',views.servicos_json,name='servicos_json'),
    path('sair/',views.logout_view,name='logout'),
    path('',lambda request: redirect('login')),
    path('servico/<int:servico_id>/', views.servico_view, name='servico'),
    path('servico/<int:servico_id>/anexar/', views.upload_arquivo, name='anexar_arquivo'),
    path('anexo/<int:anexo_id>/delete/', views.deletar_anexo, name='deletar_anexo'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm_view.html"), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),


]