from django import forms
from .models import Transaccion, Categoria, Cartera

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Comida, Transporte, Sueldo...'
                }
            ),
        }
        labels = {
            'nombre': 'Nombre de la Categoría',
        }

class CarteraForm(forms.ModelForm): # Nueva clase CarteraForm
    class Meta:
        model = Cartera
        fields = ['nombre', 'saldo_inicial']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Efectivo, Banco Principal, Tarjeta de Crédito...'
                }
            ),
            'saldo_inicial': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01', # Para permitir decimales
                    'placeholder': '0.00'
                }
            ),
        }
        labels = {
            'nombre': 'Nombre de la Cartera/Cuenta',
            'saldo_inicial': 'Saldo Inicial ($)',
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['fecha', 'tipo', 'monto', 'categoria', 'cartera', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'cartera': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'fecha': 'Fecha de la Transacción',
            'tipo': 'Tipo (Ingreso/Gasto)',
            'monto': 'Monto ($)',
            'categoria': 'Categoría',
            'cartera': 'Cartera / Cuenta',
            'descripcion': 'Descripción (Opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "Seleccione una categoría"
        self.fields['cartera'].empty_label = "Seleccione una cartera"
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['cartera'].queryset = Cartera.objects.all()