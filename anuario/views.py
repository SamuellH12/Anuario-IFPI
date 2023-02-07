from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .forms import NewUserForm, newAlunoForm, editTurmaForm, editAlunoForm, editFotoForm, newFotoForm, newPostForm, newPostitForm, newsForm
from .models import Turma, Aluno, Foto, Post, Postit

# Create your views here.

def initial_page(request):
  return redirect('quadro')

def anuario(request):
  turmas = Turma.objects.order_by('anoDaFormatura')
  temp = []
  div = 0
  
  turma = {'ano':2000, 'lista':[]}

  for t in turmas:
    if t.anoDaFormatura != turma['ano']:
      temp.append(turma.copy())
      turma['ano'] = t.anoDaFormatura
      turma["lista"] = []
      if t.anoDaFormatura < timezone.now().year - 3:
        div+=1
      
    turma['lista'].append(t)

  temp.append(turma.copy())
  temp.pop(0) #tirar a turma "professores"
  
  return render(request, 'turma_list.html', {'turmas': temp[:div+1], 'turmasC':temp[div+1:]})


def quadro(request):
  postits = Postit.objects.filter(create_date__gt =  timezone.now().date() - timedelta(days=7)).order_by('folha')
  posts = Post.objects.filter(publish_date__lt = timezone.now()).filter(noticia = False).order_by('-publish_date')
  news = Post.objects.filter( noticia = True ).filter(publish_date__lt = timezone.now()).order_by('-publish_date')
  
  return render(request, 'quadro.html', {"postits": postits, "posts" : posts, 'news' : news})


### Turma START ###

def turma_detail(request, pk):
  turma = get_object_or_404(Turma, pk=pk)
  alunos = Aluno.objects.filter(turma=turma).filter(validado = True)
  
  autores = []
  for a in alunos:
    autores.append(a.user)
    
  fotos = Foto.objects.filter( author__in = autores ).filter( galeria_da_turma = True)

  return render(request, 'turma_detail.html', {'turma': turma, 'alunos':alunos, 'fotos':fotos})


@login_required
def turma_edit(request, pk):
  turma = get_object_or_404(Turma, pk=pk)

  if request.user != turma.representante.user and request.user != turma.viceRep.user:
      return redirect("initial_page")

  if request.method == "POST":
      form = editTurmaForm(request.POST, request.FILES, instance=turma)
      if form.is_valid():
          turma.save()
          return redirect('turma_detail', pk=turma.pk)
  else:
      form = editTurmaForm(instance=turma)

  return render(request, 'edit_form_simple.html', {'form' : form} )

  
### Turma END ###
### Aluno START ###


def aluno_detail(request, pk):
  aluno = get_object_or_404(Aluno, pk=pk)

  return render(request, 'aluno_detail.html', {'aluno':aluno})


@login_required
def aluno_edit(request, pk):
  aluno = get_object_or_404(Aluno, pk=pk)

  if request.user != aluno.user:
      return redirect("initial_page")

  if request.method == "POST":
      form = editAlunoForm(request.POST, request.FILES, instance=aluno)
      if form.is_valid():
          aluno.save()
          return redirect('aluno_detail', pk=aluno.pk)
  else:
      form = editAlunoForm(instance=aluno)

  return render(request, 'edit_form_simple.html', {'form' : form} )


def aluno_fotos(request, pk):
  aluno = get_object_or_404(Aluno, pk=pk)
  fotos = Foto.objects.filter( author = aluno.user )

  return render(request, 'aluno_detail_fotos.html', {'aluno':aluno, 'fotos':fotos})


def aluno_posts(request, pk):
  aluno = get_object_or_404(Aluno, pk=pk)
  posts = Post.objects.filter( author = aluno.user ).filter(noticia = False).order_by('-publish_date')

  if request.user.is_authenticated == False or request.user != aluno.user:
    posts = posts.filter(publish_date__lt = timezone.now())

  return render(request, 'aluno_detail_posts.html', {'aluno':aluno, 'posts':posts})


def aluno_perfil(request, pk):
  aluno = get_object_or_404(Aluno, pk=pk)
  fotos = Foto.objects.filter( author = aluno.user )
  posts = Post.objects.filter( author = aluno.user ).filter(publish_date__lt = timezone.now())

  return render(request, 'turma_detail.html', {'aluno':aluno, 'fotos':fotos, 'posts':posts})

### Aluno END ###


def quemSomos(request):
  return render(request, 'quemSomos.html', {})


def register_page(request):
  
    if request.method == "POST":
      form = NewUserForm(request.POST)
      aform = newAlunoForm(request.POST, request.FILES)
      
      if form.is_valid():
        print("\n\n Form is Valid!!!\n\n")
        user = form.save()
        login(request, user)
        
        aluno = aform.save(commit=False)
        aluno.user = user
        aluno.save()
        
        messages.success(request, "Registration successful." )
        return redirect("/")
      else:
        print("\n\n Form is NOT valid!\n\n")
        return render(request, 'register.html', {'register_form' : form, 'aluno_form' : aform})
        
  
    form = NewUserForm()
    aform = newAlunoForm()
    return render(request, 'register.html', {'register_form' : form, 'aluno_form' : aform})


@login_required
def foto_edit(request, pk):
  foto = get_object_or_404(Foto, pk=pk)

  if request.user != foto.author:
      return redirect("initial_page")

  if request.method == "POST":
      form = editFotoForm(request.POST, request.FILES, instance=foto)
      if form.is_valid():
          foto.save()
          return redirect('aluno_fotos', pk=get_object_or_404(Aluno, user=request.user).pk)
  else:
      form = editFotoForm(instance=foto)

  return render(request, 'edit_form_simple.html', {'form' : form} )


@login_required
def new_foto(request):
  aluno = get_object_or_404(Aluno, user=request.user)

  if not aluno.validado:
      return redirect("initial_page")
  
  if request.method == "POST":
    form = newFotoForm(request.POST, request.FILES)
    
    if form.is_valid():
      foto = form.save(commit=False)
      foto.author = request.user
      foto.create_date = timezone.now()
      foto.save()
      return redirect('aluno_fotos', pk=get_object_or_404(Aluno, user=request.user).pk)
  else:
    form = newFotoForm()

  return render(request, 'edit_form_simple.html', {'form' : form})


@login_required
def deleteFoto(request, pk):
    foto = get_object_or_404(Foto, pk=pk)
  
    if request.user != foto.author:
      return redirect("initial_page")
      
    foto.delete()
    return redirect('aluno_fotos', pk=get_object_or_404(Aluno, user=request.user).pk)


@login_required
def new_post(request):
  
  aluno = get_object_or_404(Aluno, user=request.user)
  if not aluno.validado:
      return redirect("initial_page")
  
  if request.method == "POST":
    form = newPostForm(request.POST, request.FILES)
    
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.aluno = get_object_or_404(Aluno, user=request.user)
      post.create_date = timezone.now()
      post.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = newPostForm()

  return render(request, 'edit_form_simple.html', {'form' : form})


def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  aluno = get_object_or_404(Aluno, user=post.author)
  return render(request, 'post_detail.html', {'post':post, 'aluno':aluno})


@login_required
def deletePost(request, pk):
    post = get_object_or_404(Post, pk=pk)
  
    if request.user != post.author:
      return redirect("initial_page")
      
    post.delete()
    return redirect('aluno_posts', pk=get_object_or_404(Aluno, user=request.user).pk)


@login_required
def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)

  if request.user != post.author:
      return redirect("initial_page")

  if request.method == "POST":
      form = newPostForm(request.POST, request.FILES, instance=post)
      if form.is_valid():
          post.save()
          return redirect('post_detail', pk=post.pk)
  else:
      form = newPostForm(instance=post)

  return render(request, 'edit_form_simple.html', {'form' : form} )


@login_required
def publishPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
  
    if request.user != post.author:
      return redirect("initial_page")
      
    post.publish()
    return redirect('post_detail', pk=post.pk)



def pesquisa(request):
    alunos = []
    posts = []
    news = []
  
    if request.method == "GET":
        query = request.GET.get('search')
        if query:
          us = User.objects.filter( Q( first_name__icontains = query ) | Q( last_name__icontains = query ) )
          alunos = Aluno.objects.filter( user__in = us )
          posts = Post.objects.filter( Q(title__icontains = query) | Q(subtitle__icontains = query) ).filter(publish_date__lt = timezone.now()).filter(noticia = False)
          news = Post.objects.filter( Q(title__icontains = query) | Q(subtitle__icontains = query) ).filter(publish_date__lt = timezone.now()).filter(noticia = True)
            
    return render(request, 'search_simple.html', {'query': query, 'alunos': alunos, 'posts':posts[:6], 'news': news[:6]})



@login_required
def new_postit(request):
  aluno = get_object_or_404(Aluno, user=request.user)
  if not aluno.validado:
      return redirect("initial_page")
  
  if request.method == "POST":
    form = newPostitForm(request.POST, request.FILES)
    
    if form.is_valid():
      postit = form.save(commit=False)
      postit.author = request.user
      postit.create_date = timezone.now()
      postit.save()
      return redirect('quadro')
  else:
    form = newPostitForm()

  return render(request, 'edit_form_simple.html', {'form' : form})


@login_required
def deletePostit(request, pk):
    postit = get_object_or_404(Postit, pk=pk)
  
    if request.user != postit.author:
      return redirect("initial_page")
      
    postit.delete()
    return redirect('quadro')


@login_required
def postit_edit(request, pk):
  postit = get_object_or_404(Postit, pk=pk)

  if request.user != postit.author:
      return redirect("initial_page")

  if request.method == "POST":
      form = newPostitForm(request.POST, request.FILES, instance=postit)
      if form.is_valid():
          postit.save()
          return redirect('quadro')
  else:
      form = newPostitForm(instance=postit)

  return render(request, 'edit_form_simple.html', {'form' : form} )



def news_initial(request):
  news = Post.objects.filter( noticia = True ).filter(publish_date__lt = timezone.now()).order_by('-publish_date')

  return render(request, 'news_initial.html', {'news':news, 'manchete':news[0] })


@login_required
def new_news(request):
  aluno = get_object_or_404(Aluno, user=request.user)
  if not aluno.reporter:
      return redirect("initial_page")
  
  if request.method == "POST":
    form = newsForm(request.POST, request.FILES)
    
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.aluno = get_object_or_404(Aluno, user=request.user)
      post.create_date = timezone.now()
      post.noticia = True
      post.save()
      return redirect('news_detail', pk=post.pk)
  else:
    form = newsForm()

  return render(request, 'edit_form_simple.html', {'form' : form})


@login_required
def news_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)

  if request.user != post.author:
      return redirect("initial_page")

  if request.method == "POST":
      form = newsForm(request.POST, request.FILES, instance=post)
      if form.is_valid():
          post.save()
          return redirect('news_detail', pk=post.pk)
  else:
      form = newsForm(instance=post)

  return render(request, 'edit_form_simple.html', {'form' : form} )


def news_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  aluno = get_object_or_404(Aluno, user=post.author)
  return render(request, 'news_detail.html', {'post':post, 'aluno':aluno})
