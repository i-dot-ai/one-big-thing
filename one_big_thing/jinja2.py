import jinja2
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify
from markdown_it import MarkdownIt

markdown_converter = MarkdownIt()

DEFAULT = object()


def url(path, *args, **kwargs):
    assert not (args and kwargs)
    return reverse(path, args=args, kwargs=kwargs)


def markdown(text, cls=None):
    html = markdown_converter.render(text).strip()
    html = html.replace("<p>", f'<p class="{cls or ""}">', 1).replace("</p>", "", 1)
    return html


def is_selected(data, name, value):
    if str(data.get(name)) == str(value):
        return "selected"
    else:
        return ""


def is_in(data, name, value):
    if value in data.get(name, ()):
        return "selected"
    else:
        return ""


def is_checked(data, name, value):
    if str(data.get(name)) == str(value):
        return "checked"
    else:
        return ""


def is_empty_selected(data, name):
    if data.get(name) in ("", None):
        return "selected"
    else:
        return ""


def list_to_options(iterable):
    result = tuple({"value": item[0], "text": item[1]} for item in iterable)
    return result


def environment(**options):
    extra_options = dict()
    env = jinja2.Environment(
        **{
            "autoescape": True,
            **options,
            **extra_options,
        }
    )
    env.globals.update(
        {
            "static": static,
            "url": url,
            "is_checked": is_checked,
            "is_in": is_in,
            "is_selected": is_selected,
            "slugify": slugify,
            "list_to_options": list_to_options,
            "is_empty_selected": is_empty_selected,
            "DEFAULT": DEFAULT,
        }
    )
    return env
