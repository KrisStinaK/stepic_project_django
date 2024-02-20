from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from app.forms import AddForm, UploadFileForm
from app.models import Game, Category, TagPost, UploadFiles
from .utils import *


class GameHome(DataMixin, ListView):
    model = Game
    template_name = 'app/index.html'
    title_page = 'Главная страница'
    cat_selected = 0

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
    contact_list = Game.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'app/about.html',
                  {'title': 'О сайте',
                   'menu': menu,
                   'page_obj': page_obj})


# class AddPage(View):
#     def get(self, request):
#         form = AddForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление проекта',
#             'form': form}
#         return render(request, 'app/addpage.html', data)
#
#     def post(self, request):
#         form = AddForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         form = AddForm()
#         data = {'menu': menu,
#                 'title': 'Добавление проекта',
#                 'form': form}
#         return render(request, 'app/addpage.html', data)

# class AddPage(FormView):
#     form_class = AddForm
#     template_name = 'app/addpage.html'
#     success_url = reverse_lazy('home')
#     extra_context = {'title': 'Добавление проекта',
#                      'menu': menu}
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class AddPage(CreateView):
    form_class = AddForm
    template_name = 'app/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    extra_context = {'title': 'Добавление проекта',
                     'menu': menu}


class UpdatePage(UpdateView):
    model = Game
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'app/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактироание статьи'


class DeletePage(DeleteView):
    model = Game
    template_name = 'app/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'


def register(request):
    return render(request, 'app/register.html')


def login(request):
    return render(request, 'app/login.html')


class GameCategory(DataMixin, ListView):
    template_name = 'app/projects.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Game.published.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


def projects(request):
    posts = Game.published.all()
    data = {
        'posts': posts,
    }
    return render(request, 'app/projects.html', context=data)


class ShowPost(DataMixin, DetailView):
    template_name = 'app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Game.published, slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')



