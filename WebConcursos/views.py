from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.http import HttpResponse
from django.contrib.auth.models import User
from .import forms
from django.contrib.auth.decorators import login_required
import re
from django.contrib import messages

# Create your views here.
#registrar usuarios: metodo usado para crear el usuario en la aplicacion
def form_registrar_usuario(request):
	print("Formulario metodo post")
	if request.method == 'POST':
		formulario_registro = UserCreationForm(request.POST)
		if formulario_registro.is_valid():
			print(request.POST.get('username'))
			patron_correo = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
			cumple_patron = patron_correo.match(request.POST.get('username'))
			print(cumple_patron)
			if cumple_patron:
				#guarda el usuario en la base de datos
				user = formulario_registro.save()
				login(request,user)
				messages.success(request, 'Gracias por registrarte!!!!!')
				return redirect('agenda_eventos:login') #Lo envio a la pantalla de ingreso de usuarios ya registrados
			else:
				messages.info(request, 'El registro debe realizarse con un correo electronico valido')
	else:
		print("Formulario en blanco para creacion de usuario")
		formulario_registro = UserCreationForm()
	return render(request,'nuevo_usuario.html',{'formulario_registro':formulario_registro})

#login
def formulario_ingresar_usuario(request):
	if request.method == 'POST':
		formulario_ingreso = AuthenticationForm(data=request.POST)
		if formulario_ingreso.is_valid(): #si el usuario y password son correctos
			#login
			user = formulario_ingreso.get_user()
			login(request,user) #usado para quedar loqueado en la aplicacion de admin
			#eventos = Evento.objects.filter(username = user).order_by('fecha_inicio') #envio solo eventos del usuario login
			#return render(request, 'lista_eventos.html', {'eventos':eventos, 'usuario': user})
			return redirect('agenda_eventos:lista_eventos') #hacia urls.py para name = lista_eventos
	else:
		formulario_ingreso = AuthenticationForm()
	return render(request,'login.html',{'formulario_ingreso':formulario_ingreso})

#logout
def logout_view(request):
	logout(request)
	return redirect('WebConcursos:login') #hacia urls.py para name = lista_eventos
