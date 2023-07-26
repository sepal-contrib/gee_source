from pathlib import Path

from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import utils as su

from component import model as cm
from component import scripts as cs
from component import widget as cw


class MainTile(sw.Tile):
    def __init__(self):

        # create the model
        self.model = cm.Model()

        # generate widgets
        self.app_url = sw.TextField(v_model=None, class_="mr-3")
        self.validate = sw.Btn("validate", "mdi-check")
        self.filename = sw.TextField(v_model=None, disabled=True, class_="mr-3")
        self.save = sw.Btn("save", "mdi-content-save", disabled=True)
        self.output_window = cw.CodeWindow()
        self.computation_alert = sw.Alert()

        # link the widgets
        (self.model.bind(self.app_url, "app_url").bind(self.filename, "filename"))

        # create 2 layouts
        app = sw.Flex(
            class_="d-flex", row=True, xs12=True, children=[self.app_url, self.validate]
        )

        save = sw.Flex(
            class_="d-flex", row=True, xs12=True, children=[self.filename, self.save]
        )

        super().__init__(
            "main_tile",
            "Extract code from asset",
            inputs=[
                app,
                save,
                self.computation_alert,
                sw.Divider(class_="mt-2"),
                self.output_window,
            ],
        )

        # rewire alert
        self.alert = self.computation_alert

        # manually decorate functions
        self.on_validate = su.loading_button(self.alert, self.validate, True)(
            self.on_validate
        )
        self.on_save = su.loading_button(self.alert, self.save, True)(self.on_save)

        # js behaviour
        self.validate.on_event("click", self.on_validate)
        self.save.on_event("click", self.on_save)
        self.filename.on_event("blur", self._sanitize_filename)

    def on_validate(self, widget, event, data):

        # check inputs
        if not self.alert.check_input(self.model.app_url, "missing asset"):
            return

        # set the code in the raw value of the code
        self.model.raw_code = cs.jsext(self.model.app_url)

        # create the html output
        self.output_window.template = cs.html(self.model.raw_code)

        # free the save btn layout
        self.save.disabled = False
        self.filename.v_model = su.normalize_str(Path(self.model.app_url).name)
        self.filename.disabled = False

        return

    def on_save(self, widget, event, data):

        # check inputs
        if not self.alert.check_input(self.model.raw_code, "missing code"):
            return

        # save it
        path = cs.save(self.model.raw_code, self.model.filename)

        # tell the user it's saved
        self.computation_alert.add_msg(f'the file is saved in "{path}"', "success")

        return

    def _sanitize_filename(self, widget, event, data):
        """change the filename to ensure that only valid character are used."""
        # exit if empty
        if self.filename.v_model is None:
            return

        # else normalize it
        self.filename.v_model = su.normalize_str(self.filename.v_model)

        return
