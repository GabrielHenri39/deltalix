from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.http import HttpResponse
from .middleware import BlockedIPMiddleware
from .models import BlockedIP

class BlockedIPMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = BlockedIPMiddleware(get_response=lambda req: HttpResponse("OK"))

    def test_ip_bloqueado(self):
        ip = "127.0.0.1"
        BlockedIP.objects.create(ip_address=ip, blocked_until=timezone.now() + timezone.timedelta(hours=1))

        request = self.factory.get("/")
        request.META['REMOTE_ADDR'] = ip

        response = self.middleware(request)
        self.assertEqual(response.status_code, 403)

    def test_ip_nao_bloqueado(self):
        ip = "127.0.0.2"
        request = self.factory.get("/")
        request.META['REMOTE_ADDR'] = ip

        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_ip_expirado(self):
        ip = "127.0.0.3"
        BlockedIP.objects.create(ip_address=ip, blocked_until=timezone.now() - timezone.timedelta(hours=1))

        request = self.factory.get("/")
        request.META['REMOTE_ADDR'] = ip

        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
