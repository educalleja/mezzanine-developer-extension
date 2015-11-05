
from mezzanine.blog.views import blog_post_detail

class RedirectViews(object):

    def process_template_response(self, request, response):
        """ Replacing the response template when rendering a post detail.
        """
        if 'blog/blog_post_detail.html' in response.template_name:
            response.template_name = "blog_custom/blog_post_detail.html"
        return response