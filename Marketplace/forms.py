from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Productor, ComunidadAutonoma, Provincia
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm

class ProductorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Confirmación de contraseña')

    class Meta:
        model = Productor
        fields = ('id_regepa', 'dni_prod', 'nombre_prod', 'email', 'ccaa_prod', 'provincia_prod', 'cp_prod', 'username', 'teléfono_prod')
        labels = {
            'id_regepa': 'ID Regepa',
            'dni_prod': 'DNI',
            'nombre_prod': 'Nombre',
            'email': 'Correo electrónico',
            'cp_prod': 'Código Postal',
            'username': 'Nombre de usuario',
            'teléfono_prod': 'Teléfono',
        }
        widgets = {
            'provincia_prod': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        provincias = [(provincia.id, provincia.provincia) for provincia in Provincia.objects.all()]
        comunidades = [(comunidad.id, comunidad.nombre) for comunidad in ComunidadAutonoma.objects.all()]
        self.fields['provincia_prod'].choices = provincias
        self.fields['ccaa_prod'].choices = comunidades

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            self.add_error('password_confirmation', "Las contraseñas no coinciden")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    class Meta:
        model = Productor
        fields = ['email', 'password1']

class FiltroIndex(forms.Form):
    comunidad_autonoma = forms.ModelChoiceField(queryset=ComunidadAutonoma.objects.all(), required=False, label="Comunidad Autónoma", widget=forms.Select(attrs={'class': 'my-style'}))
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=False, label="Provincia", widget=forms.Select(attrs={'class': 'my-style'}))


class EncuestaComunicacionForm(forms.Form):
    frecuencia_uso = forms.ChoiceField(choices=(('a', 'Diariamente'), ('b', 'Semanalmente'), ('c', 'Mensualmente'), ('d', 'Menos de una vez al mes'), ('e', 'Nunca')), label='¿Con qué frecuencia utilizas la plataforma de comunicación entre productores?')
    utilidad = forms.ChoiceField(choices=(('a', 'Sí, es muy útil'), ('b', 'Sí, es útil'), ('c', 'Neutral'), ('d', 'No es muy útil'), ('e', 'No es útil en absoluto')), label='¿Encuentras útil la plataforma de comunicación entre productores?')
    eficacia = forms.ChoiceField(choices=(('a', 'Muy efectiva'), ('b', 'Efectiva'), ('c', 'Neutral'), ('d', 'No muy efectiva'), ('e', 'Ineficaz')), label='¿Cómo calificarías la eficacia de la plataforma de comunicación entre productores?')
    negocios = forms.ChoiceField(choices=(('a', 'Sí, en múltiples ocasiones'), ('b', 'Sí, en una ocasión'), ('c', 'No, pero estoy en proceso de negociación'), ('d', 'No, no he tenido éxito en los negocios')), label='¿Has realizado negocios o establecido contactos comerciales a través de la plataforma de comunicación entre productores?')

class EncuestaRegistroVentaDirectaForm(forms.Form):
    registro = forms.ChoiceField(choices=(('a', 'Sí'), ('b', 'No')), label='¿Te registraste en la plataforma para obtener información y asesoramiento sobre el proceso de inscripción en el censo de ventas de proximidad?')
    informacion = forms.ChoiceField(choices=(('a', 'Sí, toda la información necesaria estaba disponible en la plataforma'), ('b', 'No, faltaba información importante en la plataforma'), ('c', 'No me registré en la plataforma para obtener información sobre el censo')), label='¿Encontraste toda la información necesaria en la plataforma para inscribirte en el censo de ventas de proximidad?')
    facilidad = forms.ChoiceField(choices=(('a', 'Muy fácil'), ('b', 'Fácil'), ('c', 'Neutral'), ('d', 'Difícil'), ('e', 'Muy difícil')), label='¿Cómo calificarías la facilidad de uso de la plataforma para obtener información sobre el censo de ventas de proximidad?')
    recomendacion = forms.ChoiceField(choices=(('a', 'Definitivamente sí'), ('b', 'Probablemente sí'), ('c', 'No estoy seguro'), ('d', 'Probablemente no'), ('e', 'Definitivamente no')), label='¿Recomendarías la plataforma a otros agricultores que necesiten información sobre el censo de ventas de proximidad?')

class EncuestaMercadillosForm(forms.Form):
    uso = forms.ChoiceField(choices=(('a', 'Sí'), ('b', 'No')), label='¿Utilizas la plataforma para obtener información sobre los mercadillos ambulantes en la comarca y provincia?')
    utilidad = forms.ChoiceField(choices=(('a', 'Sí, es muy útil'), ('b', 'Sí, es útil'), ('c', 'Neutral'), ('d', 'No es muy útil'), ('e', 'No es útil en absoluto')), label='¿Encuentras útil la información sobre los mercadillos ambulantes en la plataforma?')
    accesibilidad = forms.ChoiceField(choices=(('a', 'Muy accesible'), ('b', 'Accesible'), ('c', 'Neutral'), ('d', 'Poco accesible'), ('e', 'Muy poco accesible')), label='¿Cómo calificarías la accesibilidad de la información sobre los mercadillos ambulantes en la plataforma?')
    participacion = forms.ChoiceField(choices=(('a', 'Sí, en múltiples ocasiones'), ('b', 'Sí, en una ocasión'), ('c', 'No, pero estoy en proceso de participación'), ('d', 'Nunca')), label='¿Has participado en un mercadillo ambulante gracias a la información proporcionada en la plataforma?')

from .models import DireccionesProd

class AddDireccionForm(forms.ModelForm):
    class Meta:
        model = DireccionesProd
        fields = ['calle', 'numero', 'codigo_postal', 'provincia', 'tipo_venta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_venta'].disabled = True

class EditDireccionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditDireccionForm, self).__init__(*args, **kwargs)
        self.fields['calle'].widget.attrs.update({'id': 'edit_id_calle'})
        self.fields['numero'].widget.attrs.update({'id': 'edit_id_numero'})
        self.fields['codigo_postal'].widget.attrs.update({'id': 'edit_id_codigo_postal'})
        self.fields['provincia'].widget.attrs.update({'id': 'edit_id_provincia'})
        self.fields['tipo_venta'].widget.attrs.update({'id': 'edit_id_tipo_venta'})

    class Meta:
        model = DireccionesProd
        fields = ['calle', 'numero', 'codigo_postal', 'provincia', 'tipo_venta']