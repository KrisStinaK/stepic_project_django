from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView

from app.forms import AddForm, UploadFileForm
from app.models import Game, Category, TagPost, UploadFiles

menu = ['О сайте', 'Главная страница', 'Обратная связь', 'Войти']


class GameHome(ListView):
    model = Game
    template_name = 'app/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Game.published.all().select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добро пожаловать на GameDevX!'
        context['menu'] = menu
        context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
        return context


def handle_uploaded_file(f):
    with open(f'uploads/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'app/about.html',
                  {'title': 'О сайте',
                   'menu': menu,
                   'form': form})


class AddPage(View):
    def get(self, request):
        form = AddForm()
        data = {
            'menu': menu,
            'title': 'Добавление проекта',
            'form': form}
        return render(request, 'app/addpage.html', data)

    def post(self, request):
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        form = AddForm()
        data = {'menu': menu,
                'title': 'Добавление проекта',
                'form': form}
        return render(request, 'app/addpage.html', data)


def register(request):
    return render(request, 'app/register.html')


def login(request):
    return render(request, 'app/login.html')


def show_post(request, post_slug):
    post = get_object_or_404(Game, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'app/post.html', data)


class GameCategory(ListView):
    template_name = 'app/projects.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Game.published.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#
#     posts = Game.published.filter(cat_id=category.pk)
#     data = {
#         'title': {category.name},
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'app/projects.html', context=data)


def projects(request):
    posts = Game.published.all()
    data = {
        'posts': posts,
    }
    return render(request, 'app/projects.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Game.Status.PUBLISHED)
    data = {
        'title': ''
    }


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')



