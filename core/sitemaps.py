from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from services.models import Servico

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home:index', 'services:service_list', 'auteticacao:login']

    def location(self, item):
        return reverse(item)
