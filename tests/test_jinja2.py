from one_big_thing.jinja2 import markdown


def test_convert_markdown_sanitises_html():
    dodgy_html = '<script>alert("Oops! This is a malicious script.");</script>'
    converted_markdown = markdown(dodgy_html)
    assert "<script>" not in converted_markdown, converted_markdown


def test_convert_markdown():
    markdown_text = "**I am bold**"
    expected = "<p><strong>I am bold</strong></p>"
    actual = markdown(markdown_text)
    assert actual == expected, actual
