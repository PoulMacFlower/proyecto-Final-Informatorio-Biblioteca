from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.contrib import messages
from django.views.generic import View, UpdateView, DeleteView
from .forms import ArticleForm
from apps.categoria.forms import CategoryForm
from .models import Articles
from apps.categoria.models import Categoria
from django.urls import reverse_lazy

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponseRedirect
from apps.usuario.models import User


# -------------------------------------- SECCION DE CATEGORIAS  -------------------------------------------


# mostrar todos los articulos desde nav articulos / mas filtos
class AllArticlesView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q')
        category_id = request.GET.get('category')
        author_id = request.GET.get('author')
        sort_by = request.GET.get('sort_by')

        articles = Articles.objects.all()

        if search_query:
            articles = articles.filter(title__icontains=search_query)

        if category_id:
            articles = articles.filter(category_id=category_id)

        if author_id:
            articles = articles.filter(author_id=author_id)

        if sort_by == 'asc':
            articles = articles.order_by('date_published')
        elif sort_by == 'desc':
            articles = articles.order_by('-date_published')

        if sort_by == 'alpha_asc':
            articles = articles.order_by('title')
        elif sort_by == 'alpha_desc':
            articles = articles.order_by('-title')

        paginator = Paginator(articles, 6)
        page_number = request.GET.get('page')

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context = {
            'page': page,
            'search_query': search_query,
            'category_id': category_id,
            'author_id': author_id,
            'sort_by': sort_by, 
            'categories': Categoria.objects.all(),
            'authors': User.objects.filter(is_colaborador=True),
        }

        return render(request, 'articles/all_articles.html', context)



# -------------------------------------- SECCION DE ARTICULOS CRUD -------------------------------------------


# para CREAR articulos / colaborador
class ArtCreateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_colaborador
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('usuarios:login_user')
        else:
            return redirect('usuarios:signup_user')

    def get(self, request, *args, **kwargs):
        form = ArticleForm(initial={'category':1})
        context = {
            'form': form
        }
        return render(request, 'articles/Art_create.html', context)
    
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                image = form.cleaned_data.get('image')
                date_published = form.cleaned_data.get('date_published')
                category = form.cleaned_data.get('category')

                if request.user.is_authenticated and request.user.is_colaborador:
                    p, created = Articles.objects.get_or_create(title=title, content=content, image=image, date_published=date_published, category=category, author=request.user)
                    p.save()
                    return redirect('home')
                else:
                    return redirect('usuarios:login_user')

        context = {}
        return render(request, 'articles/Art_create.html', context)
    

# para DETALLES de un articulos 
class ArtDetailView(View):
    def get(self, request, post_id, *args, **kwargs):
        article = get_object_or_404(Articles, pk=post_id)
        # comments = Comment.objects.filter(article=article).order_by('-id')
        # form = CommentForm()

        context = {
            'article': article,
            # 'comments': comments,
            # 'form': form,
        }
        return render(request, 'articles/Art_detail.html', context)

    def post(self, request, post_id, *args, **kwargs):
        article = get_object_or_404(Articles, pk=post_id)
        # comments = Comment.objects.filter(article=article)
        form = (request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            author = request.user
            # Comment.objects.create(article=article, author=author, content=content)
            return redirect('articulos:detail_article', post_id=post_id)

 
        context = {
            'article': article,
            # 'comments': comments,
            'form': form,
        }
        return render(request, 'articles/Art_detail.html', context)
    
    # def delete(self, request, comment_id, *args, **kwargs):
    #     comment = get_object_or_404(Comment, pk=comment_id).order_by('-id')
    #     post_id = comment.article.pk  
    #     comment.delete()
    #     return redirect('articulos:detail_article', post_id=post_id)    


# para ACTUALIZAR un artículo / colaborador
class ArtUpdateView(LoginRequiredMixin, UpdateView):
    model = Articles
    form_class = ArticleForm
    template_name = 'articles/Art_update.html'

    def test_func(self):
        return self.request.user.is_colaborador    
    
    def form_valid(self, form):
        messages.success(self.request, 'Los cambios se han guardado exitosamente.')
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('pk')
        article = get_object_or_404(Articles, pk=post_id)
        context['article'] = article
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('articulos:detail_article', kwargs={'post_id': pk})


# para ELIMINAR un artículo / colaborador
class ArtDeleteView(DeleteView):
    model = Articles
    template_name = 'articles/Art_delete.html'
    success_url = reverse_lazy('home')

