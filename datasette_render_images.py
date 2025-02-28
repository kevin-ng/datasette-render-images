from datasette import hookimpl
import base64
import imghdr
from markupsafe import Markup

DEFAULT_SIZE_LIMIT = 100 * 1024
DEFAULT_WIDTH = 300
DEFAULT_HEIGHT =300


@hookimpl
def render_cell(value, datasette):
    size_limit = DEFAULT_SIZE_LIMIT
    if datasette:
        plugin_config = datasette.plugin_config("datasette-render-images") or {}
        size_limit = plugin_config.get("size_limit") or DEFAULT_SIZE_LIMIT
        width = plugin_config.get("width") or DEFAULT_WIDTH 
        height = plugin_config.get("height") or DEFAULT_HEIGHT 
    # Only act on byte columns
    if not isinstance(value, bytes):
        return None
    # Only render images < size_limit (default 100kb)
    if len(value) > size_limit:
        return None
    # Is this an image?
    image_type = imghdr.what(None, h=value)
    if image_type not in ("png", "jpeg", "gif"):
        return None
    # Render as a data-uri
    return Markup(
        '<img src="data:image/{};base64,{}" alt="" width={} height={}>'.format(
            image_type, base64.b64encode(value).decode("utf8"), width, height
        )
    )
