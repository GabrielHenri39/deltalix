import logging
from django.shortcuts import render, redirect
from .models import Servico,AnexosServico
from .forms import ServicoForm
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.messages import constants
from .utils import enviar_email_protocolo, render_context, enviar_email_cancelamento
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.cache import cache

# cria um logger para este módulo
logger = logging.getLogger(__name__)

# Create your views here.
@require_http_methods(["GET", "POST"])
def service_list(request: HttpRequest) -> HttpResponse:
    """List all services."""
    if request.method == 'GET':
        servico_form = ServicoForm()
        logger.info("Acessando página de cadastro de serviços (GET).")
        return render(request, 'service_list.html', render_context(servico_form))

    else:
        servico_form = ServicoForm(request.POST)
        if servico_form.is_valid():
            servico: Servico = servico_form.save(commit=False)
            servico.save()
            servico_form.save_m2m()

            logger.info(f"Novo serviço cadastrado: protocolo={servico.protocolo}, id={servico.id}")

            try:
                enviar_email_protocolo(servico)
                logger.info(f"E-mail de protocolo enviado com sucesso para protocolo={servico.protocolo}")
            except Exception as e:
                logger.error(f"Erro ao enviar e-mail para protocolo={servico.protocolo}: {e}")
                messages.add_message(
                    request,
                    constants.WARNING,
                    'Serviço cadastrado com sucesso, mas não foi possível enviar o e-mail de confirmação.'
                )
                return redirect('mes_servico', protocolo=servico.protocolo)

            return redirect('mes_servico', protocolo=servico.protocolo)

        else:
            logger.warning("Erro de validação ao cadastrar serviço. Dados inválidos no formulário.")
            messages.add_message(request, constants.ERROR, 'Erro ao enviar o serviço. Verifique os dados e tente novamente.')
            return render(request, 'service_list.html', render_context(servico_form))


@require_GET
def protocolo(request: HttpRequest, protocolo: str) -> HttpResponse:
    """Display the protocol page."""
    logger.info(f"Tentando buscar serviço pelo protocolo: {protocolo}")
    try:
        servico = Servico.objects.get(protocolo=protocolo)
        logger.info(f"Serviço encontrado: protocolo={protocolo}, id={servico.id}")
        return render(request, 'mes_servico.html', {'servico': servico})
    except Servico.DoesNotExist:
        logger.warning(f"Serviço não encontrado para protocolo={protocolo}")
        messages.add_message(request, constants.ERROR, 'Serviço não encontrado.')
        return redirect('service_list')


@require_http_methods(["GET", "POST"])
def consulta_servico(request: HttpRequest) -> HttpResponse:
    """Consultar um serviço pelo protocolo."""
    protocolo = request.GET.get('protocolo') or request.POST.get('protocolo')
    servico = None
    anexos = []  # garante inicialização
    STATUS_NAO_CANCELAVEL = ['Cancelado', 'concluido', 'em_andamento']

    if protocolo:
        servico = Servico.objects.only(
            'protocolo','nome','email','status','descricao',
            'categoria','data_criacao','data_atualizacao'
        ).filter(protocolo=protocolo).first()

        if servico:
            anexos = list(AnexosServico.objects.filter(servico__protocolo=protocolo).all())
        else:
            messages.add_message(request, constants.ERROR, 'Serviço não encontrado.')

    return render(request, 'consulta_servico.html', {
        'servico': servico,
        'STATUS_NAO_CANCELAVEL': STATUS_NAO_CANCELAVEL,
        'protocolo': protocolo,
        'anexos': anexos
    })



@require_POST
def cancelar_servico(request: HttpRequest, protocolo: str) -> HttpResponse:
    """Inicia o cancelamento de um serviço."""
    try:
        servico = Servico.objects.get(protocolo=protocolo)
        STATUS_NAO_CANCELAVEL = ['Cancelado', 'concluido', 'em_andamento']

        if servico.status in STATUS_NAO_CANCELAVEL:
            mensagens = {
                'Cancelado': 'Este serviço já foi cancelado.',
                'concluido': 'Este serviço já foi concluído e não pode ser cancelado.',
                'em_andamento': 'Este serviço está em andamento e não pode ser cancelado.',
            }

            logger.warning(f"{mensagens[servico.status]} {protocolo} ")
            messages.add_message(request, constants.WARNING, mensagens[servico.status])
        else:
            enviar_email_cancelamento(servico)
            
            messages.add_message(request, constants.SUCCESS, 'E-mail de confirmação de cancelamento enviado.')

        # Redireciona de volta para a mesma consulta mantendo o protocolo
        return redirect(f'/services/consulta/?protocolo={servico.protocolo}')

    except Servico.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Serviço não encontrado.')
        return redirect('consulta_servico')


@require_GET
def cancelar_servico_confirmacao(request: HttpRequest, token: str) -> HttpResponse:
    """Confirm cancellation of a service using a token."""
    servico_id = cache.get(token)
    if not servico_id:
        messages.add_message(request, constants.ERROR, 'Token inválido ou expirado.')
        logger.warning(f"Token inválido ou expirado para cancelamento: token={token}")
        return redirect(f'/services/consulta/')

    try:
        servico = Servico.objects.get(id=servico_id)
        STATUS_NAO_CANCELAVEL = ['Cancelado', 'concluido', 'em_andamento']
        if servico.status in STATUS_NAO_CANCELAVEL:
            mensagens = {
                'Cancelado': 'Este serviço já foi cancelado.',
                'concluido': 'Este serviço já foi concluído e não pode ser cancelado.',
                'em_andamento': 'Este serviço está em andamento e não pode ser cancelado.',
            }
            messages.add_message(request, constants.WARNING, mensagens[servico.status])
            logger.info(f"Tentativa de cancelar serviço não cancelável: id={servico_id}, status={servico.status}")
            return redirect(f'/services/consulta/?protocolo={servico.protocolo}')
        else:
            servico.status = 'Cancelado'
            servico.save()
            cache.delete(token)

            messages.add_message(request, constants.SUCCESS, 'Serviço cancelado com sucesso.')
            logger.info(f"Serviço cancelado com sucesso: id={servico_id}")
            return redirect(f'/services/consulta/?protocolo={servico.protocolo}')

    except Servico.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Serviço não encontrado.')
        logger.error(f"Serviço não encontrado ao confirmar cancelamento: id={servico_id}")
        return redirect('service_list')
           