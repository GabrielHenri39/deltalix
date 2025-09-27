from django import forms
from .models import Servico, CategoriaServico
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ServicoFormAdmin(forms.ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'protocolo' in self.fields:
            self.fields['protocolo'].disabled = True

    
class CategoriaServicoForm(forms.ModelForm):
    class Meta:
        model = CategoriaServico
        fields = ['nome', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if CategoriaServico.objects.filter(nome=nome).exists():
            raise ValidationError(_('Já existe uma categoria com este nome.'))
        return nome
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            "nome", "descricao", "categoria", "email", "telefone",
            "cep", "cidade", "bairro", "rua", "numero", "complemento"
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Digite o nome do serviço"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descreva o serviço"}),
            "cep": forms.TextInput(attrs={"class": "form-control", "id": "id_cep", "placeholder": "Digite o CEP"}),
            "cidade": forms.TextInput(attrs={"class": "form-control", "id": "id_cidade"}),
            "bairro": forms.TextInput(attrs={"class": "form-control", "id": "id_bairro"}),
            "rua": forms.TextInput(attrs={"class": "form-control", "id": "id_rua"}),
            "numero": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número"}),
            "complemento": forms.TextInput(attrs={"class": "form-control", "placeholder": "Complemento (opcional)"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "exemplo@email.com"}),
            "telefone": forms.TextInput(attrs={"class": "form-control", "placeholder": "(99) 99999-9999"}),
            "categoria": forms.SelectMultiple(attrs={"class": "form-control select2"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        telefone = cleaned_data.get("telefone")

        if not email and not telefone:
            raise forms.ValidationError("Informe pelo menos um contato (e-mail ou telefone).")

        return cleaned_data
