
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from mezzanine.conf import settings


class PlainWidget(forms.Textarea):
    """
    A plain Textarea compatible with mezzanine

    """
    def __init__(self, template=None, *args, **kwargs):
        self.template = template or 'dev_widgets/editor.html'
        super(PlainWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        """ Rendering the form field using a template.
        """
        value = value if value is not None else ''
        print settings.CHECK_XHTML_SYNTAX, settings.CHECK_XHTML_INTERVAL
        print settings.REFRESH_PREVIEW_AUTO, settings.REFRESH_PREVIEW_INTERVAL
        return mark_safe(render_to_string(self.template, {
            'value': value,
            'is_admin': 'hola',
            'check_xhtml': settings.CHECK_XHTML_SYNTAX,
            'check_xhtml_s': settings.CHECK_XHTML_INTERVAL,
            'refresh_preview': settings.REFRESH_PREVIEW_AUTO,
            'refresh_preview_s': settings.REFRESH_PREVIEW_INTERVAL,
        }))

    class Media:
        """ Adding the following media to the form field template.
        """
        css = {'all': (
            'mezzanine_developer_extension/css/blog_custom_styles.css',
            'mezzanine_developer_extension/font-awesome-4.4.0/css/'
            'font-awesome.min.css',
            'mezzanine/css/smoothness/jquery-ui-1.9.1.custom.min.css',)}
        js = ('mezzanine_developer_extension/js/editor.js',
              'mezzanine/js/%s' % settings.JQUERY_FILENAME,
              'mezzanine/js/%s' % settings.JQUERY_UI_FILENAME,
              'filebrowser/js/filebrowser-popup.js')
