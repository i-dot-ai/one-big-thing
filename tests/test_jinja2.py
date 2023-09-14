from one_big_thing import jinja2


def test_convert_markdown_sanitises_html():
    dodgy_html = '<script>alert("Oops! This is a malicious script.");</script>'
    converted_markdown = jinja2.markdown(dodgy_html)
    assert "<script>" not in converted_markdown, converted_markdown


def test_convert_markdown():
    markdown_text = "**I am bold**"
    expected = "<p><strong>I am bold</strong></p>"
    actual = jinja2.markdown(markdown_text)
    assert actual == expected, actual


def test_humanize_timedelta():
    actual = jinja2.humanize_timedelta()
    assert actual == "0 minutes", actual
    actual = jinja2.humanize_timedelta(609)
    expected = "10 hours and 9 minutes"
    assert actual == expected, actual
    actual = jinja2.humanize_timedelta(13000)
    expected = "More than 200 hours"
    assert actual == expected, actual
    actual = jinja2.humanize_timedelta(609, hours_limit=2)
    expected = "More than 2 hours"
    assert actual == expected, actual
    actual = jinja2.humanize_timedelta(301, hours_limit=2, too_large_msg="too long")
    expected = "too long"
    assert actual == expected, actual
