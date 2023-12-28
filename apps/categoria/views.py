from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.contrib import messages
from django.views.generic import View, UpdateView, DeleteView
from .forms import CategoryForm
from apps.articulo.forms import ArticleForm
from .models import Categoria
from apps.articulo.models import Articles
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from apps.usuario.models import User



# -------------------------------------- SECCION DE CATEGORIAS  -------------------------------------------

# para CREAR categorias / colaborador
class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_colaborador
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('usuarios:login_user')
        else:
            return redirect('usuarios:signup_user')

    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        categories = Categoria.objects.all()

        paginator = Paginator(categories, 5)

        page_number = request.GET.get('page')

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context = {
            'form': form,
            'categories_page': page,  
        }
        return render(request, 'category/category_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria:create_category')

        categories = Categoria.objects.all()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'category/category_create.html', context)


# para ELIMINAR categorias / colaborador
class CategoryDeleteView(DeleteView):
    model = Categoria
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('categoria:create_category')


#MOSTRAR TODAS las categorias
class AllCategoriaView(View):
    def get(self, request, *args, **kwargs):
        categories = Categoria.objects.annotate(count=Count('articles'))
    
        paginator = Paginator(categories, 6)

        page_number = request.GET.get('page')

        try:
            categories_page = paginator.page(page_number)
        except PageNotAnInteger:
            categories_page = paginator.page(1)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)

        context = {
            'categories_page': categories_page
        }
        return render(request, 'category/all_category.html', context)
    

# Mostrar todos los artículos dependientes de esa categoría
class AllCategoriaArticlesView(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        try:
            category = Categoria.objects.get(pk=category_id)
            articles = category.articles_set.all()

            paginator = Paginator(articles, 3)

            page_number = request.GET.get('page')

            try:
                articles_page = paginator.page(page_number)
            except PageNotAnInteger:
                articles_page = paginator.page(1)
            except EmptyPage:
                articles_page = paginator.page(paginator.num_pages)

        except Categoria.DoesNotExist:
            articles_page = []
            category = None

        context = {
            'category': category,
            'articles_page': articles_page
        }
        return render(request, 'category/all_category_articles.html', context)


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


