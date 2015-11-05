from django import template

from django.utils.safestring import mark_safe
from mezzanine.conf import settings

from mezzanine_developer_extension.utils import refactor_html


register = template.Library()

# Checking settings.TEMPLATE_STYLE.
# Possible values are:
#   - mezzanine_developer_extension.styles.macos
#   - mezzanine_developer_extension.styles.ubuntu
#   - mezzanine_developer_extension.styles.windows
_prefix = "mezzanine_developer_extension.styles"
try:
    if settings.TERMINAL_STYLE not in \
     ["%s.macos" % _prefix, "%s.ubuntu" % _prefix, "%s.windows" % _prefix]:
        # If the user has specified a wrong terminal styling format, we
        # raise an exception warning about this.
        msg = "Wrong terminal style format. Check the value of TERMINAL_STYLE"\
              " in your settings.py file."
        raise Exception(msg)

except AttributeError:
    msg = "You have not specified a terminal output format. You have to"\
          " define the attribute TERMINAL_STYLE in your settings.py"
    raise Exception(msg)


@register.filter(name='safe_developer')
def safe_developer(content, style="macos"):
    """
    Renders content without cleaning the original.
    Replaces the terminal divs for a more complext html layout.
    """
    new_content = refactor_html(content, style)
    return mark_safe(new_content)