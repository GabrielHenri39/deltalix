from django.db import models
from random import randint
from datetime import datetime
from django.utils.text import slugify
from django.db import transaction, IntegrityError
from .exceptions import ProtocoloDuplicadoException
from django.utils import timezone
from datetime import timedelta


class CategoriaServico(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
            return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Categoria de Serviço'
        verbose_name_plural = 'Categorias de Serviços'
        


class Servico(models.Model):
    STATUS_CHOICES = [
        
        ('em_andamento', 'Em Andamento'),
        ('em_analise', 'Em Análise'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        
    ]
     
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ManyToManyField(CategoriaServico, verbose_name='Categoria', help_text='Selecione a categoria do serviço')
    email = models.EmailField(verbose_name='E-mail', help_text='E-mail para contato relacionado ao serviço')
    telefone = models.CharField(max_length=15, verbose_name='Telefone', help_text='Telefone para contato relacionado ao serviço')
    cep = models.CharField(max_length=10, verbose_name='CEP', help_text='CEP relacionado ao serviço')
    cidade = models.CharField(max_length=100, verbose_name='Cidade', help_text='Cidade relacionada ao serviço')
    bairro = models.CharField(max_length=100, verbose_name='Bairro', help_text='Bairro relacionado ao serviço')
    rua = models.CharField(max_length=100, verbose_name='Rua', help_text='Rua relacionada ao serviço')
    numero = models.CharField(max_length=10, verbose_name='Número', help_text='Número do local relacionado ao serviço')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento', help_text='Complemento do endereço relacionado ao serviço')
    ativo = models.BooleanField(default=True)
    protocolo = models.CharField(max_length=50,
                                 unique=True, blank=True, editable=False,
                                 verbose_name='Protocolo',
                                 null=True,)
    data_criacao = models.DateTimeField(auto_now_add=True,verbose_name='Data de Criação', help_text='Data em que o serviço foi criado')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização', help_text='Data da última atualização do serviço')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_analise')

    def __str__(self):
        return self.nome
    
    def gerar_protocolo_unico(self):
        for _ in range(10):  # evita loop infinito
            datetime_today = datetime.now().strftime("%d%m%Y%H%M%S%f")
            protocolo = f"PROTO-{datetime_today}-{randint(1000, 9999)}"
            if not Servico.objects.filter(protocolo=protocolo).exists():
                return protocolo
        raise ProtocoloDuplicadoException("Não foi possível gerar um protocolo único após várias tentativas.")

    
    def save(self, *args, **kwargs):
        if not self.protocolo:
            for _ in range(10):
                with transaction.atomic():
                    self.protocolo = self.gerar_protocolo_unico()
                    try:
                        return super().save(*args, **kwargs)
                    except IntegrityError:
                        continue
            raise ProtocoloDuplicadoException("Falha ao salvar: protocolo já existe após várias tentativas.")
        return super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['-data_criacao','nome']



class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    blocked_until = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    def register_attempt(self):
        """Registra uma tentativa e aplica bloqueios progressivos."""
        now = timezone.now()

        # Se a última tentativa foi há mais de 1 minuto, zera o contador
        if self.last_attempt and (now - self.last_attempt).seconds > 60:
            self.attempts = 0

        self.attempts += 1
        self.last_attempt = now

        # Se passou de 5 tentativas em 1 minuto → bloqueia progressivamente
        if self.attempts >= 5:
            if not self.blocked_until or self.blocked_until <= now:
                # Define penalidades progressivas
                if self.attempts == 5:
                    self.blocked_until = now + timedelta(hours=1)
                elif self.attempts == 10:  # reincidência
                    self.blocked_until = now + timedelta(hours=24)
                elif self.attempts == 15:
                    self.blocked_until = now + timedelta(weeks=1)
                elif self.attempts >= 20:
                    self.blocked_until = now + timedelta(days=30)

        self.save()


class AnexosServico(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexos_servico/')
    descricao = models.CharField(max_length=255, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anexo para {self.servico.nome} - {self.arquivo.name}"

    class Meta:
        verbose_name = 'Anexo de Serviço'
        verbose_name_plural = 'Anexos de Serviços'
        ordering = ['-data_upload']
