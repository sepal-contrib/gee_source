from pygments import highlight, lexers
from pygments.formatters import HtmlFormatter


def html(raw_code):
    """Format the proposed javascript code using pygments."""
    # convert into html code
    formatter = HtmlFormatter()
    lex = lexers.get_lexer_by_name("javascript")
    formated_code = highlight(raw_code, lex, formatter)

    # add some styling to the initial div tag
    html_style = "overflow: auto; max-height: 65vh; border-radius: 3px; border: 1px solid lightgrey;"
    old_tag = '<div class="highlight">'
    new_tag = f'<div class="highlight pa-3 mt-2" style="{html_style}">'

    formated_code = formated_code.replace(old_tag, new_tag)

    return formated_code
