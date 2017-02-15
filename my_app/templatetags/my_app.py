from django import template
from django.conf import settings

from ..webpack_loader import get_tags, get_use_hot, CACHED_TAGS


register = template.Library()


@register.simple_tag
def webpack_bundle(part='js'):
    if get_use_hot():
        # return only js bundle because css is included
        # and injected into <head> via js
        return get_tags(use_hot=True, part='js') if part == 'js' else ''
    if settings.DEBUG:
        # get last build because webpack is not running
        return get_tags(use_hot=False, part=part)
    # return cached tags from process lifetime, hopefully (see `webpack_loader.py`)
    return CACHED_TAGS.get(part, '')
