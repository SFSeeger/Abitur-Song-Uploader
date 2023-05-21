import bleach
from bleach.css_sanitizer import CSSSanitizer
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="range")
def template_range(a, b, sep=1):
    return range(a, b, sep)


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


css_sanitizer = CSSSanitizer(
    allowed_css_properties=["color", "font-weight", "background-color", "text-align"]
)


@register.filter(name="bleach")
def template_bleach(i):
    return mark_safe(
        bleach.clean(
            i,
            tags=settings.ALLOWED_TAGS,
            attributes=settings.ALLOWED_ATTRIBUTES,
            css_sanitizer=css_sanitizer,
        )
    )
