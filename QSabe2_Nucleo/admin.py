from django.contrib import admin
from QSabe2_Nucleo.models import *

# Register your models here.
class QuestoesAdmin(admin.ModelAdmin):
    pass

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "questoes", "criador", "dtCriacao"]
    list_filter = ["questoes", "criador"]

class RespostaAdmin(admin.ModelAdmin):
    search_fields = ["titulo", "criador"]
    list_display = ["titulo", "pergunta", "criador", "dtCriacao"]

admin.site.register(Questoes, QuestoesAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta, RespostaAdmin)