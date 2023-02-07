from django.urls import path
from . import views

urlpatterns = [
    path('', views.initial_page, name='initial_page'),
    path('anuario', views.anuario, name='anuario'),
    path('quadro', views.quadro, name='quadro'),
    path('turma/<int:pk>/', views.turma_detail, name='turma_detail'),
    path('turma/<int:pk>/edit', views.turma_edit, name='turma_edit'),
    path('aluno/<int:pk>/', views.aluno_detail, name='aluno_detail'),
    path('aluno/<int:pk>/edit', views.aluno_edit, name='aluno_edit'),
    path('aluno/<int:pk>/fotos', views.aluno_fotos, name='aluno_fotos'),
    path('aluno/<int:pk>/posts', views.aluno_posts, name='aluno_posts'),
    path('foto/<int:pk>/edit', views.foto_edit, name='foto_edit'),
    path('foto/<int:pk>/delete', views.deleteFoto, name='foto_delete'),
    path('foto/newFoto', views.new_foto, name='new_foto'),
    path('blog/newPost', views.new_post, name='new_post'),
    path('blog/<int:pk>/', views.post_detail, name='post_detail'),
    path('blog/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('blog/<int:pk>/delete', views.deletePost, name='post_delete'),
    path('blog/<int:pk>/publish', views.publishPost, name='post_publish'),
    path('quadro/newPostit', views.new_postit, name='new_postit'),
    path('quadro/<int:pk>/edit', views.postit_edit, name='postit_edit'),
    path('quadro/<int:pk>/delete', views.deletePostit, name='postit_delete'),
    path('quem', views.quemSomos, name="quem"),
    path('news', views.news_initial, name="news_initial"),
    path('news/<int:pk>', views.news_detail, name="news_detail"),
    path('news/newNews', views.new_news, name="new_news"),
    path('news/<int:pk>/edit', views.news_edit, name="news_edit"),
    path("register/", views.register_page, name="register"),
    path("pesquisar", views.pesquisa, name="pesquisa" )
]