
import os
from io import StringIO

from lxml import etree as ET
from lxml.etree import XMLSyntaxError
from lxml import html

current_path = os.path.dirname(os.path.realpath(__file__))

def readFile(path):
    """ Returns the String contained in the file passed by parameter.

    Returns:
      str: File content on a single string line.
    """
    try:
        with open(path, 'r') as fd:
            out = ''.join(fd.readlines())
            fd.close()
        return out
    except IOError:
        raise

def path_template(template_name):
    """ Returns the absolute path of the template.
    """
    path = os.path.join(current_path, "templates")
    absolute_path = "{}/{}".format(path, template_name)
    return absolute_path


def replace_labels_string(element, label, newstring):
    """ Replaces in the text of Element and its childs the text label for
    newstring
    """
    # When the element does not have children, we replace the string in the
    # element text.
    if len(element) == 0:
        element.text = element.text.replace(label, newstring)
    else:
        for child in element:
            replace_labels_string(child, label, newstring)


def replace_labels_element(element, label, elements):
    """ Replaces the label in element for elements
    """
    if len(element) == 0:
        # Deleting the original label.
        element.text = element.text.replace(label,'')
        # Inserting the new children.
        for e in elements:
            element.append(e)
    else:
        for child in element:
            replace_labels_element(child, label, elements)


def get_new_terminal_template(style):
    """ Returns a lxml Element containing the new terminal layout.
    """
    template_name = "{}.template".format(style)
    template_path = path_template(template_name)
    new_terminal = ET.parse(template_path)
    return new_terminal.find("div")


def refactor_terminals(xhtml, style):
    """ Searches all divs whose class='terminal' and replaces it by a 
    group of divs that will be used to render the terminal in the blog post.
    """
    terminals_in_post = xhtml.xpath("//div[@class='terminal']")
    i = 1
    for terminal in terminals_in_post:
        parent_object = terminal.getparent()
        terminal_title = terminal.get("title", "")
        terminal_li = terminal.getchildren()  # Obtaining li elements

        # Obtaining a copy of a new clean terminal
        new_terminal = get_new_terminal_template(style)
        replace_labels_string(new_terminal, "__TITLE__", terminal_title)
        replace_labels_element(new_terminal, "__COMMANDS__", terminal_li)

        parent_object.replace(terminal, new_terminal)
        i = i + 1


def refactor(xhtml, style):
    """ Refactors the xhtml structure. Refactors the following elements:
            - div class='terminal macos'
            - div class='code'

    Attributes:
      xhtml (ET.Element): Original blog post xhtml code.
      style (str): Indicates the output style: macos, windows or ubuntu.
    """
    # Changing the structure for divs whose class is terminal.
    refactor_terminals(xhtml, style)


def prefactor(content):
    content = content.replace(u"\xa0", u" ")
    return content


def refactor_html(content, style='macos'):
    """ Generates the HTML output for the blog.

    Attributes:
      data (str): Un-cleaned HTML data to be displayed at the blog entry.
      style (str): Determines the output style. Valid values: 'macos',
        'ubuntu','windows'
    """
    # Applying first modifications to the content.
    content = prefactor(content)

    # As we are going to process xml, we need the blog content within a
    # root element. This root element will be <blogpost></blogpost>
    # It will be removed on the final output.
    content_prestore = "<blogpost>{}</blogpost>".format(content)
    root = html.fromstring(content_prestore)

    refactor(root, style)

    # Removing the blogpost envelope.
    result = ET.tostring(root)
    return result.replace("<blogpost>", "").replace("</blogpost>", "")


def is_valid_xhtml(content):
    """ Returns a tuple specifying whether the content passed by parameter is 
    valid xhtml code. When the string is not valid xhtml, the second element
    in the tuple contains the error message from the parser. 
    """
    try:
        ET.parse(StringIO(unicode(content)))
    except XMLSyntaxError as e:
        return (False, e.message)
    return (True, '')
