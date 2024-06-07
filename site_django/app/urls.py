from django.urls import path, re_path, register_converter, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.GameHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('posts/<slug:post_slug>', views.ShowPost.as_view(), name='posts'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('category/<slug:cat_slug>', views.GameCategory.as_view(), name='category'),
    path('addproject/', views.AddPage.as_view(), name='addproj'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.DeletePage.as_view(), name='delete_page')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

