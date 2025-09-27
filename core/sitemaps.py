from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from services.models import Servico

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [ 'home', 'contato', 'service_list', 'consulta_servico']

    def location(self, item):
        return reverse(item)
