from qtpy.QtWidgets import QWidget


class Properties(QWidget):
    def __init__(self, napari_viewer="napari.viewer.Viewer()"):
        super().__init__()
