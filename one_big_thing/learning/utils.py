import enum
import functools
import inspect
import types

import marshmallow
from django.http import HttpResponseNotAllowed

from one_big_thing.learning import models
from one_big_thing.settings import ALLOWED_CIVIL_SERVICE_DOMAINS

event_names = set()


class Interface:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        all_event_names = tuple(
            event_name for entity in kwargs.values() for event_name in getattr(entity, "event_names", ())
        )
        if len(all_event_names) != len(set(all_event_names)):
            raise DuplicateEvent(all_event_names)
        self.event_names = all_event_names


class MethodDispatcher:
    def __new__(cls, request, *args, **kwargs):
        view = super().__new__(cls)
        method_name = request.method.lower()
        method = getattr(view, method_name, None)
        if method:
            return method(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(request)


class ChoicesMeta(enum.EnumMeta):
    """A metaclass for creating a enum choices."""

    def __new__(metacls, classname, bases, classdict, **kwds):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if isinstance(value, (list, tuple)) and len(value) > 1 and isinstance(value[-1], str):
                value, label = value
            elif hasattr(value, "name"):
                label = str(value.name)
            else:
                label = value
                value = key
            labels.append(label)
            # Use dict.__setitem__() to suppress defenses against double
            # assignment in enum's classdict.
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        for member, label in zip(cls.__members__.values(), labels):
            member._label_ = label
        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    @property
    def names(cls):
        return tuple(member.name for member in cls)

    @property
    def choices(cls):
        return tuple((member.name, member.label) for member in cls)

    @property
    def labels(cls):
        return tuple(label for _, label in cls.choices)

    @property
    def values(cls):
        return tuple(value for value, _ in cls.choices)

    @property
    def options(cls):
        return tuple({"value": value, "text": text} for value, text in cls.choices)

    @property
    def mapping(cls):
        return dict(tuple(cls.choices))


class Choices(enum.Enum, metaclass=ChoicesMeta):
    """Class for creating enumerated choices."""

    @types.DynamicClassAttribute
    def label(self):
        return self._label_

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return super().__eq__(other)
        return self.value == other

    def __hash__(self):
        return hash(self._name_)


def is_civil_service_email(email):
    email = email.lower()
    email_split = email.split("@")
    allowed = (email_split[-1] in ALLOWED_CIVIL_SERVICE_DOMAINS)
    if not allowed:
        ALLOWED_CIVIL_SERVICE_DOMAINS_DOT = [f".{domain}" for domain in ALLOWED_CIVIL_SERVICE_DOMAINS]
        allowed = email.endswith(tuple(ALLOWED_CIVIL_SERVICE_DOMAINS_DOT))
        # Means we get subdomains eg `@engineering.dwp.gov.uk` in addition to `@dwp.gov.uk`
    return allowed


def get_arguments(func, *args, **kwargs):
    """Calculate what the args would be inside a function"""
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    arguments = bound_args.arguments
    return arguments


def _register_event(event_name, arguments):
    event_names.add(event_name)
    arguments = {key: value for (key, value) in arguments.items() if key != "self"}
    event = models.Event(name=event_name, data=arguments)
    event.save()


def resolve_schema(schema):
    """Allow either a class or an instance to be passed"""
    if isinstance(schema, marshmallow.schema.SchemaMeta):
        schema = schema()
    return schema


def register_event(event_name):
    def _decorator(func):
        func.event_name = event_name

        @functools.wraps(func)
        def _inner(*args, **kwargs):
            arguments = get_arguments(func, *args, **kwargs)
            _register_event(event_name, arguments)
            return func(*args, **kwargs)

        return _inner

    return _decorator


def process_self(func, arguments):
    """Remove `self` from arguments and bind it to func"""
    if "self" in arguments:
        func = functools.partial(func, arguments["self"])
        arguments = {k: v for k, v in arguments.items() if k != "self"}
    return func, arguments


def apply_schema(schema, data, load_or_dump):
    """Apply a schema to some data"""
    if not schema:
        return data
    if load_or_dump not in ("load", "dump"):
        raise ValueError(f"Unknown value {load_or_dump}")
    if schema:
        schema = resolve_schema(schema)
        arguments = getattr(schema, load_or_dump)(data)
    return arguments


def with_schema(default=None, load=None, dump=None):
    """Applies the load_schema.load on the arguments to the function,
    and dump_schema.dump on the result of the function.

    This ensures that validation has been passed and that the result of the
    function is JSON serialisable"""
    load_schema = load or default
    dump_schema = dump or default

    def _decorator(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            arguments = get_arguments(func, *args, **kwargs)
            bound_func, arguments = process_self(func, arguments)
            arguments = apply_schema(load_schema, arguments, "load")
            result = bound_func(**arguments)
            result = apply_schema(dump_schema, result, "dump")
            return result

        return _inner

    return _decorator


class DuplicateEvent(Exception):
    pass


class Facade:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        all_event_names = tuple(
            event_name for entity in kwargs.values() for event_name in getattr(entity, "event_names", ())
        )
        if len(all_event_names) != len(set(all_event_names)):
            raise DuplicateEvent(all_event_names)
        self.event_names = all_event_names


class Entity:
    def __init__(self):
        possible_methods = (getattr(self, key) for key in dir(self) if not key.startswith("_"))
        possible_event_names = (getattr(item, "event_name", None) for item in possible_methods)
        self.event_names = tuple(item for item in possible_event_names if item)
