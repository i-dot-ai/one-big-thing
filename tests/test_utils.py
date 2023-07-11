import datetime
import itertools

import marshmallow
from nose.tools import assert_raises

from one_big_thing.learning import utils


def test_get_arguments():
    def flibble(woz, flim="flam"):
        assert False

    result = utils.get_arguments(flibble, "floop")
    assert result == {"woz": "floop", "flim": "flam"}, result

    result = utils.get_arguments(flibble, "foo", "bar")
    assert result == {"woz": "foo", "flim": "bar"}, result

    result = utils.get_arguments(flibble, flim="blam", woz="flooble")
    assert result == {"woz": "flooble", "flim": "blam"}, result


def test_resolve_schema():
    class MySchema(marshmallow.Schema):
        thing = marshmallow.fields.String()

    result = utils.resolve_schema(MySchema)
    assert isinstance(result, marshmallow.Schema)

    result = utils.resolve_schema(MySchema())
    assert isinstance(result, marshmallow.Schema)


def test_process_self():
    def flibble(self, baz):
        return {"self": self, "baz": baz}

    data = {"self": "flam", "bimble": "burble"}
    func, arguments = utils.process_self(flibble, data)
    assert func("floop") == {"self": "flam", "baz": "floop"}
    assert arguments == {"bimble": "burble"}

    data = {"booble": "flooble"}
    func, arguments = utils.process_self(flibble, data)
    assert func("flipp", "floop") == {"self": "flipp", "baz": "floop"}
    assert arguments == {"booble": "flooble"}


def test_apply_schema():
    class MySchema(marshmallow.Schema):
        date = marshmallow.fields.Date()

    result = utils.apply_schema(MySchema, {"date": "2012-04-01"}, "load")
    expected = {"date": datetime.date(2012, 4, 1)}
    assert result == expected

    result = utils.apply_schema(MySchema, {"date": datetime.date(2012, 4, 1)}, "dump")
    expected = {"date": "2012-04-01"}
    assert result == expected

    with assert_raises(ValueError):
        result = utils.apply_schema(MySchema, {"date": datetime.date(2012, 4, 1)}, "wibble")


def test_choices():
    class MadeUp(utils.Choices):
        A = "a"
        B = "b"
        C = "c"

    expected_choices = (("A", "a"), ("B", "b"), ("C", "c"))
    expected_names = ("A", "B", "C")
    expected_values = ("A", "B", "C")
    expected_labels = ("a", "b", "c")
    expected_options = ({"value": "A", "text": "a"}, {"value": "B", "text": "b"}, {"value": "C", "text": "c"})
    expected_mapping = {"A": "a", "B": "b", "C": "c"}
    assert MadeUp.choices == expected_choices, MadeUp.choices
    assert MadeUp.names == expected_names, MadeUp.names
    assert MadeUp.values == expected_values, MadeUp.values
    assert MadeUp.labels == expected_labels, MadeUp.labels
    assert MadeUp.options == expected_options, MadeUp.options
    assert MadeUp.mapping == expected_mapping, MadeUp.mapping


def test_dictify():
    res = utils.dictify({"flibble": 1}, (("flibble", 2), ("flooble", 3)), baz=4)
    expected = {"flibble": 2, "flooble": 3, "baz": 4}
    assert res == expected, (res, expected)

    @utils.dictify
    def do_numbers(num):
        counter = itertools.count()
        for i in range(0, num, 5):
            yield str(i), next(counter)

    res = do_numbers(11)
    expected = {"0": 0, "5": 1, "10": 2}
    assert res == expected, (res, expected)
