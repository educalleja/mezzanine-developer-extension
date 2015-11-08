
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django import forms
from mezzanine.conf import settings
from .utils import readFile, path_template

class PlainWidget(forms.Textarea):
    """
    A plain Textarea compatible with mezzanine

    """
    def __init__(self, template=None, is_demo=False, *args, **kwargs):
        self.template = template or 'dev_widgets/editor.html'
        self.is_demo = is_demo
        super(PlainWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs={}):
        """ Rendering the form field using a template.
        """
        value = value if value is not None else ''
        return mark_safe(render_to_string(self.template, {
            'value': value,
            'is_demo': self.is_demo,
            'check_xhtml': settings.CHECK_XHTML_SYNTAX,
            'check_xhtml_s': settings.CHECK_XHTML_INTERVAL,
            'refresh_preview': settings.REFRESH_PREVIEW_AUTO,
            'refresh_preview_s': settings.REFRESH_PREVIEW_INTERVAL,
        }))

    def _media(self):

        css = (
            'mezzanine_developer_extension/css/blog_custom_styles.css',
            'mezzanine_developer_extension/font-awesome-4.4.0/css/'
            'font-awesome.min.css',
            'mezzanine/css/smoothness/jquery-ui-1.9.1.custom.min.css')
        js = ['mezzanine_developer_extension/js/editor.js',
              'mezzanine/js/%s' % settings.JQUERY_FILENAME,
              'mezzanine/js/%s' % settings.JQUERY_UI_FILENAME]
        if not self.is_demo:
            # We load the filebrowser javascript only on the admin area.
            # We do not want a live demo user to browse files with it.
            js.append('filebrowser/js/filebrowser-popup.js')

        return forms.Media(css={'all': css},
                           js=tuple(js))

    media = property(_media)

    # class Media:
    #     """ Adding the following media to the form field template.
    #     """
    #     css = {'all': (
    #         'mezzanine_developer_extension/css/blog_custom_styles.css',
    #         'mezzanine_developer_extension/font-awesome-4.4.0/css/'
    #         'font-awesome.min.css',
    #         'mezzanine/css/smoothness/jquery-ui-1.9.1.custom.min.css',)}
    #     js = ('mezzanine_developer_extension/js/editor.js',
    #           'mezzanine/js/%s' % settings.JQUERY_FILENAME,
    #           'mezzanine/js/%s' % settings.JQUERY_UI_FILENAME,
    #           'filebrowser/js/filebrowser-popup.js')


class PlainWidgetDemo(PlainWidget):
    """
    A plain Textarea compatible with mezzanine

    """

    def __init__(self, *args, **kwargs):
        """ Creating the form based on the PlainWidget used in the admin area 
        """
        # When the post preview is enabled, the widget will parse the code
        # automatically. This is only allowed to be done in the admin area.
        # Here we modify a flag in order to allow this behaviour only for
        # PlainWidgetDemo. However, forms containing PlainWidget will only
        # submit their data to the server in the admin area.
        super(PlainWidgetDemo, self).__init__(is_demo=True, *args, **kwargs)


class DemoForm(forms.Form):
    initial_val = readFile(path_template("demo.template"))
    code = forms.CharField(initial=initial_val, widget=PlainWidgetDemo)
