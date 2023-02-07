import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from tinymce.models import HTMLField
#==========================================================#


def path_and_renameTurma(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(instance), ext)
    return os.path.join('images/turmas', filename)

tradutor = {'INF':"Informática", 'ADM':'Administração', 'M':'Manhã', 'T':'Tarde', 'N':'Noite'}

class Turma(models.Model):
    anoDaFormatura = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    turno = models.CharField(max_length=1, choices=[('M', 'Manhã'), ('T', 'Tarde'),('N', 'Noite')])
    curso = models.CharField(max_length=3, choices=[('INF', 'Informática'), ('ADM', 'Administração')], default='INF')
    descricao = HTMLField(blank=True)
    foto = models.ImageField(upload_to=path_and_renameTurma, default='images/turmas/default_turma.png')
    representante = models.ForeignKey('Aluno', on_delete=models.RESTRICT, blank=True, null=True, related_name='representante')
    viceRep = models.ForeignKey('Aluno', on_delete=models.RESTRICT,   blank=True, null=True, related_name='viceRep')

    def getTurno(self):
        return str(self.curso)

    def __str__(self):
      if self.anoDaFormatura == 2000:
        return "Professor"
      return tradutor[self.getTurno()] + ' ' + tradutor[self.turno] + ' ' + str(self.anoDaFormatura)


#==========================================================#


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(instance.user), ext)
    return os.path.join('images/alunos/perfil', filename)


class Aluno(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    foto = models.ImageField(upload_to=path_and_rename, default='images/alunos/perfil/default_profile.png')
    turma = models.ForeignKey(Turma, on_delete=models.RESTRICT)
    bio = models.CharField(max_length=150, blank=True)
    descricao = HTMLField(blank=True)
    validado = models.BooleanField(default=False)
    reporter = models.BooleanField(default=False)

    @property
    def full_name(self):
      return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        if len(self.user.first_name) > 0:
            return self.user.first_name + ' ' + self.user.last_name
        else:
            return str(self.user)


#==========================================================#


def path_and_renameFoto(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.author.id, ext)
    return os.path.join('images/fotos', filename)


class Foto(models.Model):
    foto = models.ImageField(upload_to=path_and_renameFoto)
    descricao = models.CharField(max_length=400, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    galeria_da_turma = models.BooleanField(default=False)

#==========================================================#

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.SET_DEFAULT, default=1 )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=400, default=" ")
    text = HTMLField()
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)
    noticia = models.BooleanField(default=False)
    capa = models.ImageField(upload_to='images/posts', default='images/logos/news_default.jpg')
    

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Postit(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  text = HTMLField()
  folha = models.CharField(max_length=1, choices=[('P', 'Post-it'), ('F', 'Folha')], default='P')
  create_date = models.DateTimeField(default=timezone.now)
  

  
#==========================================================#


#futuro
class Comentario(models.Model):
    texto = models.CharField(max_length=100)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


#==========================================================#