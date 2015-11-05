
from mezzanine.conf import settings


def styles(request):
    context_data = dict()
    context_data['terminal_style'] = settings.TERMINAL_STYLE.split(".")[-1]
    return context_data