import ipyvuetify as v
from traitlets import Unicode


class CodeWindow(v.VuetifyTemplate):
    """Code_window display pure html."""

    template = Unicode(
        """
        <div class="highlight">
            <pre></pre>
        </div>
    """
    ).tag(sync=True)
