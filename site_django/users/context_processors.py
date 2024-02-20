from app.utils import menu


def get_app_context(request):
    return {'mainmenu': menu}

