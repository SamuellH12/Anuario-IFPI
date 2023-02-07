from django.contrib import admin
from .models import Aluno, Turma, Foto, Post, Postit


@admin.action(description='Valida a conta dos alunos selecionados')
def validar_aluno(modeladmin, request, queryset):
    queryset.update(validado=True)

class AlunoAdmin(admin.ModelAdmin):
    list_display = [ '__str__', 'user', 'turma', 'validado', 'reporter']
    actions = [validar_aluno]

class TurmaAdmin(admin.ModelAdmin):
  list_display = ['__str__', 'curso', 'turno', 'anoDaFormatura']
  ordering = ['anoDaFormatura']

class PostAdmin(admin.ModelAdmin):
  list_display = ['__str__', 'author', 'aluno', 'noticia']

class FotoAdmin(admin.ModelAdmin):
  list_display = ['__str__', 'author', 'galeria_da_turma']

class PostitAdmin(admin.ModelAdmin):
  list_display = ['__str__', 'author', 'create_date']

  
# Register your models here.
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Foto, FotoAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Postit, PostitAdmin)