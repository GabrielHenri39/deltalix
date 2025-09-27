from django.http import HttpResponseForbidden,HttpRequest,HttpResponse
from django.utils import timezone
from .models import BlockedIP
from typing import Callable


class BlockedIPMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        ip = self.get_client_ip(request)
        blocked_entry = BlockedIP.objects.filter(ip_address=ip).first()
        

        if blocked_entry:
            if blocked_entry.blocked_until and  blocked_entry.blocked_until > timezone.now():
                return HttpResponseForbidden("Acesso negado.")
            elif blocked_entry.blocked_until and blocked_entry.blocked_until <= timezone.now():
                blocked_entry.blocked_until = None
                blocked_entry.save(update_fields=["blocked_until"])

        return self.get_response(request)

    def get_client_ip(self, request: HttpRequest) -> str:
        """ Captura o IP real do cliente, considerando proxy/reverse proxy. """
        x_forwarded_for :str = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        return ip


