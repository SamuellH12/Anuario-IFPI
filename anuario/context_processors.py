from django.shortcuts import get_object_or_404
from .models import Aluno


def getAlunoUser(request):
  if(request.user.is_authenticated):
    aluno = get_object_or_404(Aluno, user=request.user)
    return {'alunoUser':aluno}
    
  return {'alunoUser':{'pk':0}}