import os
import simplejson as json
import socket

from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = {
    'js': '<script type="text/javascript" src="{}"></script>',
    'css': '<link type="text/css" href="{}" rel="stylesheet" />'
}
HOT_SERVER = 'http://127.0.0.1:1337/{}'


def _check_webpack_running(port=1337):
    """check if webpack is running"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    return result == 0


def get_use_hot():
    return _check_webpack_running() and settings.DEBUG


def get_bundle_data():
    """load stats from `webpack-bundle-tracker`"""
    return json.load(open(os.path.join(BASE_DIR, 'webpack-stats.json')))


def get_bundles():
    """return bundle file names"""
    bundle_data = get_bundle_data()
    return {
        'js': [b['name'] for b in bundle_data['chunks']['main']
               if b['name'].endswith('.js')],
        'css': [b['name'] for b in bundle_data['chunks']['main']
                if b['name'].endswith('.css')],
    }


def get_tags(bundles=None, use_hot=None, part='js'):
    if not bundles:
        bundles = get_bundles()
    if use_hot is None:
        use_hot = get_use_hot()
    _bundles = bundles[part]
    if use_hot:
        return mark_safe('\n'.join(
            [TEMPLATES[part].format(HOT_SERVER.format(b)) for b in _bundles]
        ))
    return mark_safe('\n'.join(
        [TEMPLATES[part].format(static('/'.join((part, b)))) for b in _bundles]
    ))


# cache for wsgi process lifetime - hopefully?? FIXME
CACHED_BUNDLES = get_bundles()
CACHED_TAGS = {
    'js': get_tags(CACHED_BUNDLES, False),
    'css': get_tags(CACHED_BUNDLES, False, 'css')
}
