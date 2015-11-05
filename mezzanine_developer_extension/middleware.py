
from mezzanine.blog.views import blog_post_detail

class RedirectViews(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ When rendering a blog post we use our custom detail template.
        This template includes the template filter to parse the html and
        provide the terminal code.
        """

        if view_func == blog_post_detail:
            view_kwargs['template'] = "blog_custom/blog_post_detail.html"