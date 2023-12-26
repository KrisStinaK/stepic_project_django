from django.urls import path, re_path, register_converter, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.GameHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('posts/<slug:post_slug>', views.show_post, name='posts'),
    path('projects/', views.projects, name='projects'),
    path('category/<slug:cat_slug>', views.GameCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.show_tag_postlist, name='tag'),
    path('addproject/', views.AddPage.as_view(), name='addproj')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

