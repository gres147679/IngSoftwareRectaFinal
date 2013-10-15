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
