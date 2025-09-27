from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView, RedirectView
from error import views as error_views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.templatetags.static import static as tag_static

sitemaps = {
    'static': StaticViewSitemap,
}
favicon_view = RedirectView.as_view(url=tag_static('common/favicon/favicon.ico'), permanent=True)

urlpatterns = [
    path('favicon.ico', favicon_view),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('services/', include('services.urls')),
    path('auth/', include('auteticacao.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml',sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]

handler400 = error_views.erro_400
handler404 = error_views.erro_404
handler403 = error_views.erro_403
handler500 = error_views.erro_500


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
