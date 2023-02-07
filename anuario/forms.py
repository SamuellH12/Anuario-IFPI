from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Aluno, Turma, Foto, Post, Postit
from tinymce.widgets import TinyMCE

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class newAlunoForm(forms.ModelForm):

  class Meta:
    model = Aluno
    fields = ('foto', 'turma')


class editAlunoForm(forms.ModelForm):

  class Meta:
    model = Aluno
    fields = ('foto', 'bio', 'descricao')

    def __init__(self, *args, **kwargs):
        super(editAlunoForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].widget = TinyMCE(attrs={'id': 'tinymce',})


class editTurmaForm(forms.ModelForm):
  class Meta:
    model = Turma
    fields = ('descricao', 'foto')
  
  def __init__(self, *args, **kwargs):
        super(editTurmaForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].widget = TinyMCE(attrs={'id': 'tinymce',})


class newFotoForm(forms.ModelForm):
  class Meta:
    model = Foto
    fields = ('foto', 'galeria_da_turma', 'descricao')


class editFotoForm(forms.ModelForm):
  class Meta:
    model = Foto
    fields = ('galeria_da_turma', 'descricao')


class newPostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'subtitle', 'text')
  
  def __init__(self, *args, **kwargs):
        super(newPostForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = TinyMCE(attrs={'id': 'tinymce',})

class newsForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'subtitle', 'capa', 'text')
  
  def __init__(self, *args, **kwargs):
        super(newsForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = TinyMCE(attrs={'id': 'tinymce',})



class newPostitForm(forms.ModelForm):
  class Meta:
    model = Postit
    fields = ('text', 'folha')
  
  def __init__(self, *args, **kwargs):
        super(newPostitForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = TinyMCE(attrs={'id': 'tinymce',})