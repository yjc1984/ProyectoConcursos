from django.contrib import admin
from django.conf.urls import url
from WebConcursos import views

app_name = 'WebConcursos'

urlpatterns = [
    url(r'user/signup/',views.form_registrar_usuario, name = 'registro'),
    #url(r'user/signup/',views.form_empleado, name = 'registro'),
    url(r'user/login/',views.formulario_ingresar_usuario, name = 'login'),
    url(r'user/logout/',views.logout_view, name = 'logout'),
	url(r'concursos/lista/',views.traer_lista_concursos, name = 'lista_concursos'),
	#url(r'crearconcurso/',views.formulario_crear_concurso, name = 'crear_concurso'),
	#url(r'^(?P<id_evento>[\w-]+)/$',views.traer_detalle_evento, name = 'detalle_evento'),
    #url(r'^borrar/(?P<id_evento>\d+)/$',views.borrar_evento, name = 'borrar'),
    #url(r'^editar/(?P<id_evento>\d+)/$',views.formulario_editar_evento, name = 'editar'),


]
