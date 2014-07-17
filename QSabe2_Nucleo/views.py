from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from QSabe2_Nucleo.models import Questoes, Pergunta, Resposta
import summarize
import nltk

def main(request):
    questoes = Questoes.objects.all()
    context = dict(questoes=questoes, user=request.user)
    return render(request, 'lista.html', context)

def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def questao(request, pk):
    """Lista as perguntas"""
    perguntas = Pergunta.objects.filter(questoes=pk).order_by('-dtCriacao')
    context = dict(perguntas=perguntas, pk=pk)
    return render(request, 'perguntas.html',context)

def pergunta(request, pk):
    """Lista todas as respostas de uma pergunta"""
    respostas = Resposta.objects.filter(pergunta=pk).order_by("-dtCriacao")
    titulo = Pergunta.objects.get(pk=pk).titulo
    explicacao = Pergunta.objects.get(pk=pk).explicacao
    tags = Pergunta.objects.get(pk=pk).tags
    context = dict(respostas=respostas, pk=pk, titulo=titulo, explicacao=explicacao, tags=tags)
    return render(request, 'respostas.html', context)

def postar(request, ptipo, pk):
    """Exibe um form de post generico"""
    acao = reverse("QSabe2_Nucleo.views.%s" % ptipo, args=[pk])
    if ptipo == "nova_pergunta":
        titulo = "Nova Pergunta"
        destino = ''
    elif ptipo == "responder":
        titulo = "Responder"
        destino = "Resposta: " + Pergunta.objects.get(pk=pk).titulo
    context = dict(destino=destino,acao=acao,titulo=titulo)
    return render(request, 'postar.html', context)

def nova_pergunta(request, pk):
    """Inicia uma nova pergunta"""
    p = request.POST
    if p["destino"] and p["conteudo"]:
        questao = Questoes.objects.get(pk=pk)
        #agente de tokenizacao, tagging, removedor de stopwords
        tokenizada = nltk.word_tokenize(p["destino"])
        emtags = nltk.tag.pos_tag(tokenizada)
        stopwords = nltk.corpus.stopwords.words('portuguese')
        filtered_words = [w for w in emtags if w not in stopwords]
        substantivos = [word for word,pos in filtered_words if pos == 'NNP' or pos == 'NNS']
        tags = [w for w in substantivos if w not in stopwords]
        pergunta = Pergunta.objects.create(questoes=questao, titulo=p["destino"], explicacao=p["conteudo"], tags=tags, \
                                           criador=request.user)
    return HttpResponseRedirect(reverse("QSabe2_Nucleo.views.questao", args=[pk]))

def responder(request, pk):
    """Responde a uma pergunta"""
    p = request.POST
    if p["conteudo"]:
        pergunta = Pergunta.objects.get(pk=pk)
        titulo = summarize.summarize_text(p["conteudo"])
        titulo = titulo.summaries
        titulo = titulo[0]
        resposta = Resposta.objects.create(pergunta=pergunta, titulo=titulo, texto=p["conteudo"], criador=request.user)
    return HttpResponseRedirect(reverse("QSabe2_Nucleo.views.pergunta", args=[pk]) + "?page=last")