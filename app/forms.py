import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import DetalleFactura, Empleado, Factura, Usuario


class RegistroForm(UserCreationForm):

    telefono = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 0991234567',
            'pattern': '[0-9]{10}',
            'maxlength': '10',
            'title': 'Ingrese exactamente 10 numeros',
        })
    )

    pregunta_seguridad = forms.ChoiceField(
        choices=Usuario.PREGUNTAS
    )

    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'telefono',
            'password1',
            'password2',
            'pregunta_seguridad',
            'respuesta_seguridad'
        ]

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if not re.fullmatch(r'\d{10}', telefono):
            raise ValidationError('El telefono debe tener exactamente 10 numeros.')

        return telefono


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'apellidos_nombres',
            'cedula_pasaporte',
            'cargo',
            'fecha_ingreso',
            'sueldo',
            'decimo_tercer_sueldo_modalidad',
            'decimo_cuarto_sueldo_modalidad',
        ]
        widgets = {
            'apellidos_nombres': forms.TextInput(attrs={'placeholder': 'Ej: Juan Perez'}),
            'cedula_pasaporte': forms.TextInput(attrs={'placeholder': 'Ej: 1723456789'}),
            'cargo': forms.TextInput(attrs={'placeholder': 'Ej: MENSAJERO'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'sueldo': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'decimo_tercer_sueldo_modalidad': forms.Select(),
            'decimo_cuarto_sueldo_modalidad': forms.Select(),
        }

    def clean_sueldo(self):
        sueldo = self.cleaned_data.get('sueldo')
        if sueldo is not None and sueldo <= 0:
            raise ValidationError('El sueldo debe ser mayor a 0.')
        return sueldo


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            'razon_social',
            'ruc',
            'direccion',
            'establecimiento',
            'punto_emision',
            'cliente_nombre',
            'cliente_identificacion',
            'tipo_identificacion',
            'cliente_direccion',
            'forma_pago',
            'tiempo_pago',
            'correo',
            'telefono',
            'fecha_emision',
        ]
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'establecimiento': forms.TextInput(attrs={'maxlength': '3'}),
            'punto_emision': forms.TextInput(attrs={'maxlength': '3'}),
            'tiempo_pago': forms.TextInput(attrs={'placeholder': 'Ej: 30 días'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 0999999999'}),
        }


class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = [
            'codigo',
            'descripcion',
            'cantidad',
            'precio_unitario',
            'descuento',
            'total_sin_impuestos',
        ]
        widgets = {
            'cantidad': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'descuento': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'total_sin_impuestos': forms.NumberInput(attrs={'step': '0.01', 'readonly': 'readonly'}),
        }


DetalleFacturaFormSet = inlineformset_factory(
    Factura,
    DetalleFactura,
    form=DetalleFacturaForm,
    extra=1,
    can_delete=True,
)
