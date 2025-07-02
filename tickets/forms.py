from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    fecha_esperada = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    prioridad = forms.ChoiceField(
        choices=[
            ('Bajo', 'Bajo'),
            ('Medio', 'Medio'),
            ('Importante', 'Importante')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    archivo = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Ticket
        fields = ['solicitante', 'email', 'titulo', 'descripcion', 'fecha_esperada', 'prioridad', 'etiqueta', 'archivo']
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'titulo': forms.TextInput(attrs={'class': 'form-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'etiqueta': forms.TextInput(attrs={'class': 'form-input'}),
        }