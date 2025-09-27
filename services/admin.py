from django.contrib import admin
from .models import Servico, CategoriaServico, BlockedIP,AnexosServico
from .forms import ServicoFormAdmin, CategoriaServicoForm

# Register your models here.

@admin.register(CategoriaServico)
class CategoriaServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'slug')
    
    form = CategoriaServicoForm
    search_fields = ('nome',)
    list_filter = ('nome',)
    readonly_fields = ('slug',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'status', 'data_criacao',)
    list_filter = ('ativo', 'status', 'data_criacao')
    search_fields = ('nome', 'descricao', 'categoria__nome')
    form = ServicoFormAdmin

    def get_readonly_fields(self, request, obj = ...):
        if obj:
            return self.readonly_fields + ('data_criacao', 'data_atualizacao', 'protocolo')
        return self.readonly_fields
    


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocked_until',)
    search_fields = ('ip_address',)
    list_filter = ('blocked_until',)
    readonly_fields = ('attempts', 'last_attempt',)

# @admin.register(AnexosServico)
# class AnexosServicoAdmin(admin.ModelAdmin):
#     list_display = ('servico', 'file', 'uploaded_at',)
#     search_fields = ('servico__nome',)
#     list_filter = ('uploaded_at',)
#     readonly_fields = ('uploaded_at',)

admin.site.register(AnexosServico)