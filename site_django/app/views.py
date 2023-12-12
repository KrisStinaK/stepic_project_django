from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from app.forms import AddForm
from app.models import Game, Category, TagPost

menu = ['О сайте', 'Главная страница', 'Обратная связь', 'Войти']


def index(request):
    data = {'title': 'Добро пожаловать на GameDevX!',
            'menu': menu,
            'cat_selected': 0,
            'y': ['Тетрис', '2048', 'Змейка', 4, 5, 6, 7, 8],
        }
    return render(request, 'app/index.html', context=data)


def about(request):
    return render(request, 'app/about.html', {'title': 'О сайте', 'menu': menu})


def addproject(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            try:
                Game.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления проекта')
    else:
        form = AddForm()
    data = {
        'menu': menu,
        'title': 'Добавление проекта',
        'form': form
    }
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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)

    posts = Game.published.filter(cat_id=category.pk)
    data = {
        'title': {category.name},
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'app/projects.html', context=data)


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



