# mezzanine-developer-extension
===============================

**mezzanine-developer-extension** provides a few features especially useful for blogs
related to information technologies, and more specifically, to programming and
system administration. Removes the wysiwyg editor and provides a few handful
shortcuts to generate terminal-looking divisions, tip bubbles and log divisions.

Overview
--------

Features:

- Removes wysiwig editor from the blog post writing form.
- Checks the html validity of the written blog post.
- Preview area in the blog post writing form.
- Add ubuntu and mac os terminal windows on your blog posts only writing a simple line of code.

Requirements:

- django >= 1.8 (only tested with this version)
- mezzanine >= 4.0.1
- lxml >= 3.0

Mezzanine
---------

Mezzanine is a content management platform built using the Django
framework. It is BSD licensed and designed to provide both a
consistent interface for managing content, and a simple, extensible
architecture that makes diving in and hacking on the code as easy as
possible.

Visit the Mezzanine project page to see some of the great sites
people have built using Mezzanine.

http://mezzanine.jupo.org

Installation
------------

**mezzanine-developer-extension** should be installed using pip:

    
    pip install git+https://github.com/educalleja/mezzanine-developer-extension
    

Quick start
-----------

1. Add "mezzanine_developer_extension" to your INSTALLED_APPS setting like this::

    ```````````````
    INSTALLED_APPS = (
        ...,
        "mezzanine_developer_extension"
    )
    ```````````````
    
2. Add the following settings to your settings.py:

    ```````````````
    TERMINAL_STYLE = "mezzanine_developer_extension.styles.ubuntu"
    RICHTEXT_WIDGET_CLASS = "mezzanine_developer_extension.widgets.PlainWidget"
    ```````````````

3. Add "mezzanine_developer_extension.middleware.RedirectViews" to the MIDDLEWARE_CLASSES setting in the project settings.py file.

    ```````````````
    MIDDLEWARE_CLASSES = (
        ...
        "mezzanine_developer_extension.middleware.RedirectViews",
        )
    ```````````````

4. Add "mezzanine_developer_extension.context_processors.styles" to the TEMPLATE_CONTEXT_PROCESSORS setting:

    ```````````````
    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        "mezzanine_developer_extension.context_processors.styles",
        )
    ```````````````

5. Include the app URLconf in your project urls.py like this::

    `("^%s" % settings.BLOG_SLUG, include("mezzanine_developer_extension.urls")),`

    **Important!**
  
     Add the previous line before the main mezzanine url include:

      `("^", include("mezzanine.urls")),`

6. Include

7. Restart server.

8. Check the new widget to write blog post in the admin area.

Configuration
--------------

It is necessary to add the following options to your settings.py

- TERMINAL_STYLE = "mezzanine_developer_extension.styles.ubuntu" for ubuntu terminal style. "mezzanine_developer_extension.styles.macos" for Mac OS X terminal style.
- RICHTEXT_WIDGET_CLASS = "mezzanine_developer_extension.widgets.PlainWidget"

**Optional configuration**

- CHECK_XHTML_SYNTAX: Enables the XHTML validator when editing a blog post. Default is True
- CHECK_XHTML_INTERVAL: Defines the interval in seconds between xhtml validations. Default is 15.
- REFRESH_PREVIEW_AUTO: Enables automatic preview updates editing a post entry. Default is False
- REFRESH_PREVIEW_INTERVAL: Defines the interval in seconds between preview updates. Default is 15

Contributing
-----------

Development of mezzanine-developer-extension happens at github: https://github.com/educalleja/mezzanine-developer-extension

Live example
------------

Find an example of a blog post written with the extension enabled on mezzanine on the following blog post:
http://www.educalleja.es/blog/example-mezzanine-developer-extension

License
-------

Copyright (C) 2015 Eduardo Calleja.
This program is licensed under the MIT License (see LICENSE)