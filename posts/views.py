from django.contrib import messages
from django.db.models import Case, Count, Q, When
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from comentarios.forms import FormComentario
from comentarios.models import Comentario

from .models import Post

# Create your views here.


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Define a orderm de como os resultados retornados
        ao context_object_name = 'posts' para serem
        ordenados pelo ID
        """
        query_set = super().get_queryset()
        query_set = query_set.order_by('-id').filter(publicado_post=True)

        query_set = query_set.annotate(
            numero_comentarios=Count(
                Case(
                    When(
                        comentario__publicado_comentario=True, then=1
                    )
                )
            )
        )

        return query_set


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        query_set = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return query_set

        query_set = query_set.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__icontains=termo)
        )

        return query_set


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        query_set = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return query_set

        query_set = query_set.filter(
            categoria_post__nome_cat__iexact=categoria)

        return query_set


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado_comentario=True,
                                                post_comentario=post.id)

        contexto['comentarios'] = comentarios

        return contexto

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)

        comentario.post_comentario = post

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentario enviado com sucesso !!')

        return redirect('post_detalhes', pk=post.id)
