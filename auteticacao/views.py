from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.views.decorators.http import require_http_methods
from .decortors import login_required_404
from django.core.paginator import Paginator
from services.models import Servico,CategoriaServico, AnexosServico
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('admin_list')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_list')  
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'login.html')

@login_required_404
def admin_list_view(request: HttpRequest) -> HttpResponse:
        categorias = CategoriaServico.objects.all()
        
        return render(request, 'admin_list.html',{'categorias': categorias})

@login_required_404
def servicos_json(request: HttpRequest) -> JsonResponse:
    pagina = request.GET.get('page', 1)
    servicos_qs = Servico.objects.all().order_by('-data_criacao')

    # Nome
    nome = request.GET.get('nome')
    if nome:
        servicos_qs = servicos_qs.filter(nome__icontains=nome)

    # Status
    status = request.GET.get('status')
    if status:
        servicos_qs = servicos_qs.filter(status=status)

    # Categorias múltiplas
    categorias = request.GET.getlist('categorias')  # pega lista do Select2
    if categorias:
        
        servicos_qs = servicos_qs.filter(categoria__id__in=categorias).distinct()


    # Datas
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    if data_inicio and data_fim:
        servicos_qs = servicos_qs.filter(data_criacao__date__range=[data_inicio, data_fim])

    # Paginação
    paginator = Paginator(servicos_qs, 10)
    try:
        servicos_page = paginator.page(pagina)
    except:
        servicos_page = paginator.page(1)

    servicos = []
    for servico in servicos_page:
        categorias = [c.nome for c in servico.categoria.all()]
        servicos.append({
            'id': servico.id,
            'protocolo': servico.protocolo,
            'nome': servico.nome,
            'email': servico.email,
            'telefone': servico.telefone,
            'categorias': categorias,
            'status': servico.get_status_display(),
            'data_criacao': servico.data_criacao.strftime('%d/%m/%Y %H:%M'),
        })

    return JsonResponse({
        'servicos': servicos,
        'num_pages': paginator.num_pages,
        'current_page': servicos_page.number,
        
       
        
    })


@login_required_404
@require_http_methods(["GET"])    
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required_404
@require_http_methods(["GET", "POST"])
def servico_view(request: HttpRequest, servico_id: int) -> HttpResponse:
    if request.method == 'GET':
        servico = get_object_or_404(Servico, id=servico_id)
        anexos = AnexosServico.objects.filter(servico=servico)
        
        status_dict = dict(Servico.STATUS_CHOICES)

        return render(request, 'servico.html', {'servico': servico, 'status_dict': status_dict, 'anexos': anexos})
    elif request.method == 'POST':
        servico = get_object_or_404(Servico, id=servico_id)
        novo_status = request.POST.get('status')
        if novo_status in dict(Servico.STATUS_CHOICES):
            try:
                servico.status = novo_status
                servico.save()
                messages.add_message(request, constants.SUCCESS, 'Status atualizado com sucesso.')
                return redirect('servico', servico_id=servico.id)
            except Exception as e:
                messages.add_message(request, constants.ERROR, 'Erro ao atualizar o status.')
                return redirect('servico', servico_id=servico.id)
        else:
            messages.add_message(request, constants.ERROR, 'Status inválido.')
            return redirect('servico', servico_id=servico.id)
        

def upload_arquivo(request: HttpRequest, servico_id: int) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        servico = get_object_or_404(Servico, id=servico_id)
        try:
            anexos = AnexosServico(servico=servico, arquivo=arquivo)
            anexos.save()
            messages.add_message(request, constants.SUCCESS, 'Arquivo enviado com sucesso.')
            return redirect('servico', servico_id=servico.id)
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro ao enviar o arquivo.')
            return redirect('servico', servico_id=servico.id)
    
        

def deletar_anexo(request: HttpRequest, anexo_id: int) -> HttpResponse:
    if request.method == 'POST':
        anexo = get_object_or_404(AnexosServico, id=anexo_id)
        servico_id = anexo.servico.id
        try:
            anexo.arquivo.delete()  # Deleta o arquivo do sistema de arquivos
            anexo.delete()  # Deleta o registro do banco de dados
            messages.add_message(request, constants.SUCCESS, 'Anexo deletado com sucesso.')
            return redirect('servico', servico_id=servico_id)
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro ao deletar o anexo.')
            return redirect('servico', servico_id=servico_id)