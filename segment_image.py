import napari
import skimage
from cellpose import models
from napari.layers import Labels
from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from skimage.util import img_as_float


def apply_cellpose(
    input_img: "napari.layers.Image",
    use_gpu: bool = True,
) -> "napari.layers.Labels":

    # Convert to float
    img = img_as_float(input_img.data)

    # Instantiate Cellpose model
    model = models.CellposeModel(gpu=use_gpu)

    # Obtain Cellpose labels
    labels, __, __ = model.eval(img)

    return Labels(labels, name=f"{input_img.name}_cellpose")


class SegmentImage(QWidget):
    def __init__(self, napari_viewer="napari.viewer.Viewer"):
        super().__init__()
        self.viewer = napari_viewer

        # Set widget layout
        self.setLayout(QVBoxLayout())

        # Add logo
        logo_widget = QWidget()
        logo_widget.setLayout(QHBoxLayout())
        logo_path = "Analyst/Day1/napari-plugin/Practicals/institut_pasteur_logo.jpg"
        logo_img = QPixmap(logo_path)
        logo_size_inner = QSize(220, 70)
        logo_size_outer = QSize(230, 80)
        logo_img = logo_img.scaled(
            logo_size_inner, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation
        )
        logo_label = QLabel()
        logo_label.setPixmap(logo_img)
        logo_label.setFixedSize(logo_size_outer.width(), logo_size_outer.height())
        logo_widget.layout().addWidget(logo_label)
        self.layout().addWidget(logo_widget)

        # Select image layer
        layer_widget = QWidget()
        layer_widget.setLayout(QHBoxLayout())
        layer_label = QLabel("Input image")
        self._image_layers = QComboBox(self)
        layer_widget.layout().addWidget(layer_label)
        layer_widget.layout().addWidget(self._image_layers)
        self.layout().addWidget(layer_widget)

        # use_gpu parameter widget
        self.gpu_widget = QWidget()
        self.gpu_widget.setLayout(QHBoxLayout())
        gpu_label = QLabel("Use GPU")
        self.gpu_checkbox = QCheckBox()
        self.gpu_checkbox.setChecked(True)
        self.gpu_widget.layout().addWidget(gpu_label)
        self.gpu_widget.layout().addWidget(self.gpu_checkbox)
        self.layout().addWidget(self.gpu_widget)

        # Run plugin
        run_btn = QPushButton("Measure")
        run_btn.clicked.connect(self._run_segmentation)
        self.layout().addWidget(run_btn)

        self._update_combo_box()

    def _update_combo_box(self):
        for layer_name in [
            self._image_layers.itemText(i) for i in range(self._image_layers.count())
        ]:
            layer_name_index = self._image_layers.findText(layer_name)
            self._image_layers.removeItem(layer_name_index)

        for layer in [
            l for l in self.viewer.layers if isinstance(l, napari.layers.Image)
        ]:
            if layer.name not in [
                self._image_layers.itemText(i)
                for i in range(self._image_layers.count())
            ]:
                self._image_layers.addItem(layer.name)

    def _get_selected_image_layer(self):
        return self.viewer.layers[self._image_layers.currentText()]

    def _run_segmentation(self):
        input_img = self._get_selected_image_layer()
        use_gpu = self.gpu_checkbox.isChecked()

        labels = apply_cellpose(
            input_img=input_img,
            use_gpu=use_gpu,
        )

        self.viewer.add_layer(labels)


if __name__ == "__main__":
    IMAGE2D = skimage.data.cells3d()[30, 1]
    viewer = napari.view_image(IMAGE2D)
    widget = SegmentImage(napari_viewer=viewer)
    viewer.window.add_dock_widget(widget)
    napari.run()
