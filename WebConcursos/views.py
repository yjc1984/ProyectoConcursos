from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.models import User
from .import forms
from django.contrib.auth.decorators import login_required
import re
from django.contrib import messages
from .models import Concurso

# Create your views here.
#registrar usuarios: metodo usado para crear el usuario en la aplicacion
def form_registrar_usuario(request):
	if request.method == 'POST':
		print(request.POST)
		formulario_registro = forms.UserRegisterFormCustom(request.POST)
		print(formulario_registro.errors.as_data())
		if formulario_registro.is_valid():
			print("Formulario valido")
			patron_correo = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
			cumple_patron = patron_correo.match(request.POST.get('username'))
			print(cumple_patron)
			if cumple_patron:
				user = formulario_registro.save(commit=False) #crea el elemnto, lo captura sin dar commit para modificar campos
				user.save()
				login(request,user)
				messages.success(request, 'Gracias por registrarte!!!!!')
				messages.success(request, 'El username para ingreso a la aplicacion es ')
				messages.success(request, user.username)
				return redirect('WebConcursos:login') #Lo envio a la pantalla de ingreso de usuarios ya registrados
			else:
				messages.info(request, 'El registro debe realizarse con un correo electronico valido')
	else:
		print("Formulario en blanco para creacion de usuario")
		formulario_registro = forms.UserRegisterFormCustom()
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
			return redirect('WebConcursos:lista_concursos') #hacia urls.py para name = lista_eventos
	else:
		formulario_ingreso = AuthenticationForm()
	return render(request,'login.html',{'formulario_ingreso':formulario_ingreso})

#logout
def logout_view(request):
	logout(request)
	return redirect('WebConcursos:login') #hacia urls.py para name = lista_eventos

#Ordena los eventos por la fecha de inicio del mismo
def traer_lista_concursos(request):
	id_usuario = User.objects.get(username = request.user).id
	nombre_usuario = User.objects.get(username = request.user).first_name
	apellido_usuario = User.objects.get(username = request.user).last_name
	concursos = Concurso.objects.filter(id_administrador = id_usuario).order_by('fecha_inicio')
	return render(request, 'lista_concursos.html', {'concursos':concursos , 'nombre_usuario':nombre_usuario, 'apellido_usuario':apellido_usuario})
