from django.contrib import admin
from django.conf.urls import url
from WebConcursos import views
from django.urls import path

app_name = 'WebConcursos'

urlpatterns = [
    url(r'user/login/',views.formulario_ingresar_usuario, name = 'login'),
    url(r'user/logout/',views.logout_view, name = 'logout'),
    url(r'user/signup/',views.form_registrar_usuario, name = 'registro'),
	url(r'concursos/lista/',views.traer_lista_concursos, name = 'lista_concursos'),
	url(r'concursos/crearconcurso/',views.formulario_crear_concurso, name = 'crear_concurso'),
	url(r'^concursos/(?P<id_concurso>[\w-]+)/$',views.traer_detalle_concurso, name = 'detalle_concurso'),
    url(r'^concursos/borrar/(?P<id_concurso>\d+)/$',views.borrar_concurso, name = 'borrar'),
    url(r'^concursos/editar/(?P<id_concurso>\d+)/$',views.formulario_editar_concurso, name = 'editar'),
    url(r'^concursos/locutor/detalle_concurso/(?P<id_concurso>[\w-]+)/(?P<id_usuario>[\w-]+)/$',views.detalle_concurso_locutor, name = 'detalle_locutor'),
	url(r'url/(?P<url_usuario>[\w:/.@+-]+)', views.resolver_url, name='resolver'),

]
