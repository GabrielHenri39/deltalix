from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import CategoriaServico , Servico
from django.conf import settings
import uuid

def get_cache_categorias() -> list:
    """
    Retrieve the list of service categories from cache or database.
    If not found in cache, fetch from the database and store in cache.
    """
    categorias = cache.get('categorias_servicos')
    
    if not categorias:
        categorias = CategoriaServico.objects.all()
        cache.set('categorias_servicos', categorias, 3600)  # Cache for 1 hour
    
    return categorias


def render_context(servico_form) -> dict:
    """Cria contexto base para o template."""
    categorias = get_cache_categorias()
    return {
        'categorias': categorias,
        'servico_form': servico_form
    }

def enviar_email_protocolo(servico: Servico) -> None:
    """Envia e-mail com protocolo para o cliente."""
    assunto = 'Seu Protocolo foi Gerado'
    mensagem_html = render_to_string('emails/protocolo_email.html', {
        'nome': servico.nome,
        'protocolo': servico.protocolo
    })

    send_mail(
        subject=assunto,
        message='',  # texto puro se desejar
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[servico.email],
        html_message=mensagem_html,
        fail_silently=False
    )

def enviar_email_cancelamento(servico: Servico) -> None:
    """Envia e-mail de confirmação de cancelamento para o cliente."""
    token = str(uuid.uuid4())
    cache.set(token, servico.id, 900)  # Token válido por 15 minutos
    link = f"{settings.SITE_URL}/services/cancelar_servico_confirmacao/{token}/"
    assunto = 'Confirme o cancelamento do seu serviço'
    mensagem_html = render_to_string('emails/cancelar_servico.html', {
        'nome': servico.nome,
        'protocolo': servico.protocolo,
        'link': link
    })

    send_mail(
        subject=assunto,
        message='',  # texto puro se desejar
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[servico.email],
        html_message=mensagem_html,
        fail_silently=False
    )