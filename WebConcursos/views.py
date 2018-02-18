from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.models import User
from .import forms
from django.contrib.auth.decorators import login_required
import re
from django.contrib import messages
from .models import Concurso, UsuarioCustom
from WebConcursos.forms import UserCreationCustom

# Create your views here.
#registrar usuarios: metodo usado para crear el usuario en la aplicacion
def form_registrar_usuario(request):
	print(request.POST.get('username'))
	if request.method == 'POST':
		#formulario_registro = forms.UserRegisterFormCustom(request.POST)
		formulario_registro = forms.UserCreationCustom(request.POST) ##funciona con nombres y apellidos pero sin empresa ni rol
		#formulario_registro = UserCreationForm(request.POST)
		formulario_registro.errors.as_data()
		if formulario_registro.is_valid():
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
		#formulario_registro = forms.UserRegisterFormCustom()
		formulario_registro = forms.UserCreationCustom() ##funciona con nombres y apellidos pero sin empresa ni rol
		#formulario_registro = UserCreationForm()
	return render(request,'nuevo_usuario.html',{'formulario_registro':formulario_registro})


#login
def formulario_ingresar_usuario(request):
	if request.method == 'POST':
		print(request.POST)
		formulario_ingreso = AuthenticationForm(data=request.POST)
		print(formulario_ingreso.errors)
		if formulario_ingreso.is_valid(): #si el usuario y password son correctos
			#login
			user = formulario_ingreso.get_user()
			login(request,user)
			return redirect('WebConcursos:lista_concursos') #hacia urls.py para name = lista_eventos
	else:
		formulario_ingreso = AuthenticationForm()
	return render(request,'login.html',{'formulario_ingreso':formulario_ingreso})

#logout
def logout_view(request):
	logout(request)
	return redirect('WebConcursos:login') #hacia urls.py para name = lista_eventos

def formulario_crear_concurso(request):
	print(request.method)
	if request.method == 'POST':
		formulario_crear = forms.FormCrearConcurso(data=request.POST)
		print(formulario_crear.errors)
		if formulario_crear.is_valid():
			concurso = formulario_crear.save(commit=False)			
			concurso.id_administrador = request.user
			concurso.save() #guardo en db
			return redirect('WebConcursos:lista_concursos' ) #despues de guardarlo, envio al usuario a la lista de eventos
	else:
		form_crear_concurso = forms.FormCrearConcurso()
		return render(request, 'crear_concurso.html', {'form_crear_concurso':form_crear_concurso})

#Ordena los concursos por la fecha de inicio del mismo
def traer_lista_concursos(request):
	concursos = Concurso.objects.filter(id_administrador = request.user).order_by('fecha_inicio')
	return render(request, 'lista_concursos.html', {'concursos':concursos})


def borrar_concurso(request, id_concurso):
	id_elegido = id_concurso
	concurso = Concurso.objects.filter(id = id_elegido)
	concurso.delete()
	current_user = request.user
	concursos = Concurso.objects.filter(id_administrador = request.user).order_by('fecha_inicio')
	return render(request, 'lista_concursos.html', {'concursos':concursos})

def traer_detalle_concurso(request, id_concurso):
	id_elegido = id_concurso
	concurso = Concurso.objects.filter(id = id_elegido)
	return render(request, 'detalle_concurso.html', {'concurso':concurso})


def formulario_editar_concurso(request, id_concurso):
	print("metodo a editar", request.method)
	if request.method == 'POST':
		formulario_edicion = forms.FormEditarConcurso(data=request.POST)
		print("formulario valido",formulario_edicion.is_valid())
		print("request.POST", request.POST)
		if formulario_edicion.is_valid():
			concurso = formulario_edicion.save(commit=False)
			concurso.id = id_concurso
			concurso.id_administrador = request.user
			concurso.save()
			return redirect('WebConcursos:lista_concursos' ) #despues de guardarlo, envio al usuario a la lista de eventos
	else:
		concursos = Concurso.objects.filter(id = id_concurso)
		print(id_concurso)
		#current_user = request.user
		formulario_edicion = forms.FormEditarConcurso()
	return render(request, 'editar_concurso.html', {'formulario_edicion':formulario_edicion , 'concursos':concursos })