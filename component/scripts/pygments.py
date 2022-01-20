from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments import lexers


def html(raw_code):
    """
    format the proposed javascript code using pygments
    """

    # convert into html code
    formatter = HtmlFormatter()
    lex = lexers.get_lexer_by_name("javascript")
    formated_code = highlight(raw_code, lex, formatter)

    return formated_code
