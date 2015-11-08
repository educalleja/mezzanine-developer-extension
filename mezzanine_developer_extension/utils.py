
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
    path = os.path.join(current_path, "templates/box_templates")
    absolute_path = "{}/{}".format(path, template_name)
    return absolute_path


def replace_labels_string(element, label, newstring):
    """ Replaces in the text of Element and its childs the text label for
    newstring
    """
    # When the element does not have children, we replace the string in the
    # element text.
    if len(element) == 0 and element.text is not None:
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


def get_template(template_name):
    """ Returns a lxml Element containing the new terminal layout.
    """
    template_path = path_template(template_name)
    new_division = ET.parse(template_path)
    return new_division.find("div")


def refactor_terminals(xhtml, style):
    """ Searches all divs whose class='terminal' and replaces it by a 
    group of divs that will be used to render the terminal in the blog post.
    """
    terminals_in_post = xhtml.xpath("//div[@class='terminal']")
    for terminal in terminals_in_post:
        parent_object = terminal.getparent()
        terminal_title = terminal.get("title", "")
        terminal_li = terminal.getchildren()  # Obtaining li elements

        # Obtaining a copy of a new clean terminal
        new_terminal = get_template("{}.template".format(style))
        replace_labels_string(new_terminal, "__TITLE__", terminal_title)
        replace_labels_element(new_terminal, "__COMMANDS__", terminal_li)

        parent_object.replace(terminal, new_terminal)


def get_code_lines(element):
    """ Returns an array of spans per line obtained from the attribute. If
    elements childs are elements, the user might be have inserted html in a
    code division. In this case. we will escape the content.
    """
    data = []
    element_children = element.getchildren()
    if len(element_children):
        text_container = "".join([ET.tostring(e) for e in element_children])
    else:
        text_container = element.text
    lines = text_container.split("\n")
    lines = lines if lines[0] != "" else lines[1:]
    lines = lines if lines[-1] != "" else lines[:-1]
    for line in lines:
        # ignoring first line if it is blank
        el = ET.Element("span")
        el.text = line
        data.append(el)
    return data


def get_text_lines(text):
    """ Returns an array of paragraph elements '<p>' for every line in the
    text passed by parameter.

    Attributes: 
        text (str): Text including break lines.

    Example:
        >>> s = "This is line\r\n And this is another line"
        >>> result = get_text_lines(text)
        >>> print result
        [<Element p>, <Element p>]
        >>> print result[0].text
        This is a line

    """
    data = []
    lines = text.split("\n")
    for line in lines:
        # ignoring first line if it is blank
        el = ET.Element("p")
        el.text = line
        data.append(el)
    return data


def refactor_codes(xhtml):
    """ Searches all divs whose class='terminal' and replaces it by a 
    group of divs that will be used to render the terminal in the blog post.
    """
    codes_in_post = xhtml.xpath("//div[@class='code']")
    for code in codes_in_post:
        parent_object = code.getparent()
        codes_lines = get_code_lines(code)

        # Obtaining a copy of a new clean terminal
        new_code_div = get_template("code.template")
        replace_labels_element(new_code_div, "__CODELINES__", codes_lines)
        parent_object.replace(code, new_code_div)


def refactor_logs(xhtml):
    """ Searches all divs whose class='logs' and replaces it by a 
    group of divs that will be used to render the terminal in the blog post.
    """
    logs_in_post = xhtml.xpath("//div[@class='log']")
    for log in logs_in_post:
        parent_object = log.getparent()
        log_lines = get_code_lines(log)

        # Obtaining a copy of a new clean terminal
        new_log_div = get_template("log.template")
        replace_labels_element(new_log_div, "__LOGLINES__", log_lines)
        parent_object.replace(log, new_log_div)


def refactor_tips(xhtml):
    """ Searches all tip elements and replaces it by a 
    group of divs that will be used to render the tip bubble in the blog post.
    """
    tips_in_post = xhtml.xpath("//div[@class='tipbox']")
    for tip in tips_in_post:
        parent_object = tip.getparent()
        tip_title = tip.get("title", "Did you know?")
        # Obtaining a copy of a new clean terminal
        new_tip_div = get_template("tip.template")
        tip_parapraphs = get_text_lines(tip.text)
        replace_labels_element(new_tip_div, "__TIPTEXT__", tip_parapraphs)
        replace_labels_string(new_tip_div, "__TIPTITLE__", tip_title)
        parent_object.replace(tip, new_tip_div)


def refactor(xhtml, style):
    """ Refactors the xhtml structure. Refactors the following elements:
            - div class='terminal macos'
            - div class='code'

    Attributes:
      xhtml (ET.Element): Original blog post xhtml code.
      style (str): Indicates the output style: macos, windows or ubuntu.
    """
    # Changing the structure for divs whose class is terminal.
    refactor_codes(xhtml)
    refactor_logs(xhtml)
    refactor_tips(xhtml)
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
