import datetime

import humanize
import jinja2
from django.conf import settings
from django.contrib import messages
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify
from markdown_it import MarkdownIt

from one_big_thing.settings import VCAP_APPLICATION

markdown_converter = MarkdownIt("js-default")  # Need js-default as secure setting

DEFAULT = object()


def url(path, *args, **kwargs):
    assert not (args and kwargs)
    return reverse(path, args=args, kwargs=kwargs)


def markdown(text, cls=None):
    html = markdown_converter.render(text).strip()
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


def humanize_timedelta(minutes=0, hours_limit=200, too_large_msg=""):
    if minutes > (hours_limit * 60):
        if not too_large_msg:
            return f"More than {hours_limit} hours"
        else:
            return too_large_msg
    else:
        delta = datetime.timedelta(minutes=minutes)
        return humanize.precisedelta(delta, minimum_unit="minutes")


def get_plausible_data_domain():
    return settings.PLAUSIBLE_DATA_DOMAIN


def get_self_hosted_plausible_address():
    return settings.SELF_HOSTED_PLAUSIBLE_ADDRESS


def environment(**options):
    extra_options = dict()
    env = jinja2.Environment(  # nosec B701
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
            "humanize_timedelta": humanize_timedelta,
            "get_messages": messages.get_messages,
            "space_name": VCAP_APPLICATION.get("space_name"),
            "PLAUSIBLE_DATA_DOMAIN": get_plausible_data_domain(),
            "SELF_HOSTED_PLAUSIBLE_ADDRESS": get_self_hosted_plausible_address(),
        }
    )
    return env
