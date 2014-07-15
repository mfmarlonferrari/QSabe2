from django.db import models
from django.contrib.auth.models import User

class Questoes(models.Model):
    titulo = models.CharField(max_length=60)

    def numPostagem(self):
        return sum([t.numPostagem() for t in self.pergunta_set.all()])

    def ultimaPostagem(self):
        if self.pergunta_set.count():
            ultima = None
            for t in self.pergunta_set.all():
                l = t.ultimaResposta()
                if l:
                    if not ultima: ultima = l
                    elif l.dtCriacao > ultima.dtCriacao: ultima = l
            return ultima

    def __unicode__(self):
        return self.titulo

class Pergunta(models.Model):
    titulo = models.CharField(max_length=60)
    dtCriacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, blank=False, null=False)
    questoes = models.ForeignKey(Questoes)

    def numPostagem(self):
        return self.resposta_set.count()

    def numResposta(self):
        return self.resposta_set.count() - 1

    def ultimaResposta(self):
        if self.resposta_set.count():
            return self.resposta_set.order_by("dtCriacao")[0]

    def __unicode__(self):
        return unicode(self.criador) + " - " + self.titulo

class Resposta(models.Model):
    titulo = models.CharField(max_length=60)
    dtCriacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, blank=False, null=False)
    pergunta = models.ForeignKey(Pergunta)
    texto = models.TextField()

    def __unicode__(self):
        return u"%s - %s - %s" % (self.criador, self.pergunta, self.titulo)

    def short(self):
        return u"%s - %s\n%s" % (self.criador, self.titulo, self.dtCriacao.strftime("%b %d, %I:%M %p"))