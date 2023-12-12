from django.contrib import admin
from django.urls import path, include
from app.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

handler404 = page_not_found


admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Добавленные игры'