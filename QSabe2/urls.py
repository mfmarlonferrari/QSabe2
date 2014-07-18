from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'login/login.html'}),
    url(r'^accounts/profile/', include(admin.site.urls)),
    url(r'^listagem/', 'QSabe2_Nucleo.views.main', name='main'),
    url(r'^(?P<pk>[0-9]+)/perguntas/$', 'QSabe2_Nucleo.views.questao', name='questao'),
    url(r'^(?P<pk>[0-9]+)/respostas/$', 'QSabe2_Nucleo.views.pergunta', name='pergunta'),
    url(r"^postar/(nova_pergunta|responder)/(\d+)/$", 'QSabe2_Nucleo.views.postar',name='postar'),
    url(r"^responder/(\d+)/$", 'QSabe2_Nucleo.views.responder',name='responder'),
    url(r"^recomendadas/", 'QSabe2_Nucleo.views.perguntaPorTags',name='recomendadas'),
    url(r"^nova_pergunta/(\d+)/$", 'QSabe2_Nucleo.views.nova_pergunta', name='nova_pergunta'),
)
