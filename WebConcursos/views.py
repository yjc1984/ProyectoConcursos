from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.models import User
from .import forms
from django.contrib.auth.decorators import login_required
import re
from django.contrib import messages
from .models import Concurso, UsuarioCustom, ListaLocutores
from WebConcursos.forms import UserCreationCustom
from django.core.mail import EmailMessage, send_mail
from django.core.files.storage import FileSystemStorage

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
			print("Request para crear concurso", request.POST)
			concurso = formulario_crear.save(commit=False)			
			concurso.id_administrador = request.user
			#concurso.ruta_imagen = 'http://localhost:8000/media/media/' + str(request.POST.get('ruta_imagen'))
			concurso.save()
			concurso.url_concurso = 'http://localhost:8000/concursos/locutor/detalle_concurso/'+ str(concurso.id) + '/' + str(concurso.id_administrador.id)
			concurso.save()
			url_usuario = concurso.url_concurso_custom
			concurso.url_concurso_custom = str(url_usuario)
			concurso.save()
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
	print("metodo  formulario_editar_concurso ", request.method)
	if request.method == 'POST':
		formulario_edicion = forms.FormEditarConcurso(request.POST, request.FILES)
		if formulario_edicion.is_valid():
			concurso = formulario_edicion.save(commit=False)
			concurso.id = id_concurso
			concurso.id_administrador = request.user
			concurso.url_concurso = 'http://localhost:8000/concursos/locutor/detalle_concurso/'
			print(concurso.ruta_imagen.url)
			concurso.save()
			concurso.url_concurso = 'http://localhost:8000/concursos/locutor/detalle_concurso/'+ str(concurso.id) + '/' + str(concurso.id_administrador.id)
			concurso.save()
			concurso.url_concurso_custom = str(concurso.url_concurso_custom)
			concurso.save()
			return redirect('WebConcursos:lista_concursos' ) #despues de guardarlo, envio al usuario a la lista de eventos
	else:
		concursos = Concurso.objects.filter(id = id_concurso)
		print(id_concurso)
		#current_user = request.user
		formulario_edicion = forms.FormEditarConcurso()
	return render(request, 'editar_concurso.html', {'formulario_edicion':formulario_edicion , 'concursos':concursos })



def detalle_concurso_locutor(request, id_concurso,id_usuario):
	id_elegido = id_concurso
	print("id_elegido", id_elegido,'id_usuario', id_usuario )
	concurso = Concurso.objects.filter(id = id_elegido, id_administrador=id_usuario)
	return render(request, 'detalle_locutor.html', {'concurso':concurso})

def resolver_url(request, url_usuario):
	print("url_usuario", url_usuario)
	if url_usuario != 'None':
		print("paso este if")
		url_oficial = Concurso.objects.all().filter(url_concurso_custom = str(url_usuario))[0].url_concurso
		print('url_oficial',url_oficial)
		if url_oficial != 'None': # si no es vacia la direccion del usuario, pero no encuentra en la consulta la url oficial
			print("Esta es la url oficial: ", url_oficial )
			return redirect(url_oficial) 
		else:
			print("No Existe la direccion configurada")
			return render(request, 'page_not_found.html')
	else: 
		print("No se ha configurado esta url por el usuario, por favor intentar la asignada por el sistema")
		return render(request, 'page_not_found.html')

def cargar(request):
	if request.method == 'POST':
		formulario_ingreso = forms.UploadFileForm(data=request.POST)
		if formulario_ingreso.is_valid(): #si el usuario y password son correctos
			foto = formulario_ingreso.save(commit=False)
			foto.save()
	else:
		formulario_ingreso = forms.UploadFileForm()
	return render(request,'upload.html',{'formulario_ingreso':formulario_ingreso})

def RegistrarLocutorView(request):
	if request.method == 'POST':
		form_lista_locutor = forms.FormListaLocutor(data=request.POST)
		if form_lista_locutor.is_valid():
			formulario = form_lista_locutor.save(commit=False)
			formulario.id_administrador = request.user
			formulario.save()
			locutores = ListaLocutores.objects.filter(id_administrador = request.user)
			form_lista_locutor = forms.FormListaLocutor()
			return render(request, 'crear_lista_locutores.html', {'form_lista_locutor':form_lista_locutor, 'locutores':locutores})
	else:
		locutores = ListaLocutores.objects.filter(id_administrador = request.user)
		form_lista_locutor = forms.FormListaLocutor()
	return render(request,'crear_lista_locutores.html',{'form_lista_locutor':form_lista_locutor, 'locutores':locutores})


def EnviarCorreoListaView(request, id_concurso):
	print("Estoy en EnviarCorreoListaView con el metodo", request.method )
	if request.method == 'POST':
		form_mensaje = forms.FormEnviarCorreo(data=request.POST)
		print("Formulario correo valido? : ", form_mensaje.is_valid())
		locutores = ListaLocutores.objects.all().filter(id_administrador = request.user)
		print(locutores.count())
		for indice in range(len(locutores)):
			print('Se enviara el concurso a : ',locutores[indice].email)

		if form_mensaje.is_valid():
			#para = request.POST.get('para')
			asunto = request.POST.get('asunto')
			mensaje = request.POST.get('mensaje')
			for indice in range(len(locutores)):
				email = EmailMessage(
							    asunto, 
							    mensaje, 
							    to=[locutores[indice].email],
								)
				email.send()
			return redirect('WebConcursos:lista_concursos')
	else:
		print('id_concurso', id_concurso)
		concurso = Concurso.objects.all().filter(id = id_concurso)
		form_mensaje = forms.FormEnviarCorreo()
	return render(request,'enviar_mail.html',{'form_mensaje':form_mensaje, 'concurso':concurso})

def BorrarLocutorView(request, id_locutor):
	id_elegido = id_locutor
	locutor = ListaLocutores.objects.filter(id = id_elegido)
	locutor.delete()
	current_user = request.user
	locutores = ListaLocutores.objects.filter(id_administrador = request.user)
	form_lista_locutor = forms.FormListaLocutor()
	return render(request, 'crear_lista_locutores.html', {'form_lista_locutor':form_lista_locutor, 'locutores':locutores})

def CrearHomeView(request):
	#Crear un div por cada usuario con concursos
	users = User.objects.all().count()
	concursos = Concurso.objects.all().count()
	print(users)
	print(concursos)
	usuarios = User.objects.all()
	concursos = Concurso.objects.all()
	for indice in range(len(usuarios)):
		print('Se creara div para : ',usuarios[indice].username)
	return render(request,'home.html',{'usuarios':usuarios ,'concursos':concursos})