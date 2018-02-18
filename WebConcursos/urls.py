from django.contrib import admin
from django.conf.urls import url
from WebConcursos import views

app_name = 'WebConcursos'

urlpatterns = [
    url(r'user/signup/',views.form_registrar_usuario, name = 'registro'),
    url(r'user/login/',views.formulario_ingresar_usuario, name = 'login'),
    url(r'user/logout/',views.logout_view, name = 'logout'),
	url(r'concursos/lista/',views.traer_lista_concursos, name = 'lista_concursos'),
	url(r'concursos/crearconcurso/',views.formulario_crear_concurso, name = 'crear_concurso'),
	url(r'^concursos/(?P<id_concurso>[\w-]+)/$',views.traer_detalle_concurso, name = 'detalle_concurso'),
    url(r'^concursos/borrar/(?P<id_concurso>\d+)/$',views.borrar_concurso, name = 'borrar'),
    url(r'^concursos/editar/(?P<id_concurso>\d+)/$',views.formulario_editar_concurso, name = 'editar'),


]
