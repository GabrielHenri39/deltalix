from django.http import Http404,HttpResponseForbidden,HttpRequest,HttpResponse
from functools import wraps 

def login_required_403(view_func):
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
    
def login_required_404(view_func):
    @wraps(view_func)
    def _wrapped_view(request:HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("Página não encontrada.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view