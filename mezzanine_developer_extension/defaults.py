from mezzanine.conf import register_setting

register_setting(
    name="CHECK_XHTML_SYNTAX",
    description="Enables the XHTML validator when editing a blog post.",
    editable=True,
    default=True,
)

register_setting(
    name="CHECK_XHTML_INTERVAL",
    description="Defines the interval in seconds between xhtml "
                "validations. Valid when CHECK_XHTML_SYNTAX=True",
    editable=True,
    default=15,
)

register_setting(
    name="REFRESH_PREVIEW_AUTO",
    description="Enables automatic preview updates editing a post entry",
    editable=True,
    default=False,
)

register_setting(
    name="REFRESH_PREVIEW_INTERVAL",
    description="Defines the interval in seconds between preview updates."
                " Valid when REFRESH_PREVIEW_AUTO=True",
    editable=True,
    default=15,
)
