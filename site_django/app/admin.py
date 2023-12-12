from django.contrib import admin, messages

from app.models import Game, Category


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'time_create', 'is_published', 'cat', 'info')
    list_display_links = ('title', )
    ordering = ['time_create']

    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title']
    list_filter = ['cat__name', 'is_published']

    @admin.display(description='Краткое описание', ordering='content')
    def info(self, game: Game):
        return f'Описание {len(game.content)} символов.'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset
        if count.is_published:
            self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Game.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


