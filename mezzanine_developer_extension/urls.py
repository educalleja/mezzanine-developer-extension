from __future__ import unicode_literals

from django.conf.urls import patterns, url

# Preview and check format urls entries.
urlpatterns = patterns("mezzanine_developer_extension.views",
    url("mezzanine_developer_extension/get_preview/$", "get_preview",
        name="get_preview"),
    url("mezzanine_developer_extension/check_format/$", "check_format",
        name="check_format"),
    url("mezzanine_developer_extension/demo_form/$", "demo_form",
        name="mzde_demo_form")
)
