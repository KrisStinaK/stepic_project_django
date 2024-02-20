from django import template
import app.views as views
from app.models import Category
from app.utils import menu

register = template.Library()


@register.simple_tag()
def get_menu():
    return menu


@register.inclusion_tag('app/list_category.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, 'cat_selected': cat_selected}


