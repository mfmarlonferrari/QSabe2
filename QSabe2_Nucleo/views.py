from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from QSabe2_Nucleo.models import Questoes, Pergunta, Resposta

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
    context = dict(respostas=respostas, pk=pk, titulo=titulo)
    return render(request, 'respostas.html', context)

def postar(request, ptipo, pk):
    """Exibe um form de post generico"""
    acao = reverse("QSabe2_Nucleo.views.%s" % ptipo, args=[pk])
    if ptipo == "nova_pergunta":
        titulo = "Nova Pergunta"
        destino = ''
    elif ptipo == "responder":
        titulo = "Responder"
        destino = "Re: " + Resposta.objects.get(pk=pk).titulo
    context = dict(destino=destino,acao=acao,titulo=titulo)
    return render(request, 'postar.html', context)

def nova_pergunta(request, pk):
    """Inicia uma nova pergunta"""
    p = request.POST
    if p["destino"] and p["conteudo"]:
        questao = Questoes.objects.get(pk=pk)
        pergunta = Pergunta.objects.create(questao=questao, titulo=p["destino"], criador=request.user)
        Resposta.objects.create(pergunta=pergunta, titulo=p["destino"], texto=p["conteudo"], criador=request.user)
    return HttpResponseRedirect(reverse("QSabe2_Nucleo.views.questao", args=[pk]))

def responder(request, pk):
    """Responde a uma pergunta"""
    p = request.POST
    if p["conteudo"]:
        pergunta = Pergunta.objects.get(pk=pk)
        resposta = Resposta.objects.create(pergunta=pergunta, titulo=p["destino"], texto=p["conteudo"], criador=request.user)
    return HttpResponseRedirect(reverse("QSabe2_Nucleo.views.pergunta", args=[pk]) + "?page=last")