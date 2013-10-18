from django import forms

#
# Agrega un cliente (form)
#
class AgregarClienteForm(forms.Form):
	cedula = forms.IntegerField(widget=forms.TextInput())
	nombrecl = forms.CharField(widget=forms.TextInput())
	direccion = forms.CharField(widget=forms.TextInput())

	def clean(self):
		return self.cleaned_data


#
# Autentica un usuario (form)
#
class loginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput()) 
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))
