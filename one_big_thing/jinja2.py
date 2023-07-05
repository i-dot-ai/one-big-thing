import jinja2
from django.templatetags.static import static
from django.urls import reverse
from markdown_it import MarkdownIt

markdown_converter = MarkdownIt()


def url(path, *args, **kwargs):
    assert not (args and kwargs)
    return reverse(path, args=args, kwargs=kwargs)


def markdown(text, cls=None):
    html = markdown_converter.render(text).strip()
    html = html.replace("<p>", f'<p class="{cls or ""}">', 1).replace("</p>", "", 1)
    return html


def environment(**options):
    extra_options = dict()
    env = jinja2.Environment(
        **{
            **options,
            **extra_options,
        }
    )
    env.globals.update(
        {
            "static": static,
            "url": url,
        }
    )
    return env
