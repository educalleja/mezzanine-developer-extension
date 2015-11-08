
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from mezzanine.conf import settings
from mezzanine_developer_extension.utils import refactor_html, is_valid_xhtml
from mezzanine_developer_extension.widgets import DemoForm

def get_preview(request):
    """ View called to generate a preview of a blog post.

    Attributes:
       request (HttpRequest): User request.

    Returns JsonResponse:
       'html_code_preview' (str): Final HTML generated from the original blog
         post.
    """
    if request.method != "POST":
        return HttpResponse(status=404)
    # Obtaining original blog content.
    post_code = request.POST.get('data')
    terminal_style = settings.TERMINAL_STYLE.split(".")[-1]
    # Generating final html from original content.
    preview_code = refactor_html(post_code, terminal_style)
    # Returing to user
    return JsonResponse({'html_code_preview': preview_code})


def check_format(request):
    """ View called to check the validity of an html blog post.

    Attributes:
      request (HttpRequest): User request.

    Returns JsonResponse:
      'formatcode' (int): 0 if original blog html is valid, 1 otherwise.
      'error_message' (str): Parse error message when blog content is not valid
        xhtml.
    """
    if request.method != "POST":
        return HttpResponse(status=404)
    post_code = request.POST.get('data')
    enveloped = "<root>{}</root>".format(post_code)
    preview_code, error_message = is_valid_xhtml(enveloped)
    return JsonResponse({'format_code': preview_code,
                         'error_message': error_message})


def demo_form(request):
    template_name = "mzz_dv_templates/widget_demo.html"
    context_data = { 'form': DemoForm()}
    return render(request, template_name, context=context_data)
