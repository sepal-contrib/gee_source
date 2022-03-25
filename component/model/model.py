from sepal_ui import model
from traitlets import Any


class Model(model.Model):

    # set up your inputs
    app_url = Any(None).tag(sync=True)
    filename = Any(None).tag(sync=True)

    # set up your outputs
    raw_code = Any(None).tag(sync=True)
