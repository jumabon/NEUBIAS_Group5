import napari
import numpy as np
from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QLabel,
                            QPushButton, QSlider, QSpinBox, QVBoxLayout,
                            QWidget)


def threshold_image(input_img: np.ndarray, threshold: float) -> np.ndarray:
    from skimage.util import img_as_float

    # Convert to float
    img = img_as_float(input_img)
    # Apply threshold
    thresh_img = img > threshold

    return thresh_img


def apply_threshold_otsu(input_img: np.ndarray, nbins: int = 256) -> np.ndarray:
    from skimage.filters import threshold_otsu
    from skimage.util import img_as_float

    # Convert to float
    img = img_as_float(input_img)
    # Obtain upper threshold value for each pixel
    threshold = threshold_otsu(img, nbins=nbins)
    # Apply thrshold
    thresh_img = img > threshold

    return thresh_img


def apply_cellpose(input_img: np.ndarray, use_gpu: bool = True) -> np.ndarray:
    from cellpose import models
    from skimage.util import img_as_float

    # Convert to float
    img = img_as_float(input_img)

    # Instantiate Cellpose model
    model = models.CellposeModel(gpu=use_gpu)

    # Obtain Cellpose labels
    labels, __, __ = model.eval(img)

    return labels


def apply_hysteresis(input_img: np.ndarray, low: float, high: float):
    from skimage.filters import apply_hysteresis_threshold
    from skimage.util import img_as_float

    img = img_as_float(input_img)

    labels = apply_hysteresis_threshold(img, low, high)
    return labels


def segment_image(
    input_img: 'napari.layers.Image',
    algorithm: str,
    threshold: float = 0.2,
    nbins: int = 256,
    use_gpu: bool = True,
    # low: float = 0.1,
    # high: float = 0.1
) -> 'napari.layers.Labels':

    from napari.layers import Labels

    if algorithm == 'Threshold':
        labels = threshold_image(input_img=input_img.data,
                                 threshold=threshold)
    elif algorithm == 'Otsu':
        labels = apply_threshold_otsu(input_img=input_img.data,
                                      nbins=nbins)
    elif algorithm == 'Cellpose':
        labels = apply_cellpose(input_img=input_img.data,
                                use_gpu=use_gpu)
    # elif algorithm == 'Hysteresis':
    #    labels = apply_hysteresis(input_img=input_img,low=low,high=high)

    return Labels(labels, name=f'{input_img.name}_{algorithm}')


class SegmentImage(QWidget):
    def __init__(self, napari_viewer='napari.viewer.Viewer'):
        super().__init__()
        self.viewer = napari_viewer

        # Set widget layout
        self.setLayout(QVBoxLayout())

        # Add logo
        logo_widget = QWidget()
        logo_widget.setLayout(QHBoxLayout())
        logo_path = 'Analyst/Day1/napari-plugin/Practicals/institut_pasteur_logo.jpg'
        logo_img = QPixmap(logo_path)
        logo_size_inner = QSize(220, 70)
        logo_size_outer = QSize(230, 80)
        logo_img = logo_img.scaled(
            logo_size_inner, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        logo_label = QLabel()
        logo_label.setPixmap(logo_img)
        logo_label.setFixedSize(logo_size_outer.width(),
                                logo_size_outer.height())
        logo_widget.layout().addWidget(logo_label)
        self.layout().addWidget(logo_widget)

        # Select image layer
        layer_widget = QWidget()
        layer_widget.setLayout(QHBoxLayout())
        layer_label = QLabel('Input image')
        self._image_layers = QComboBox(self)
        layer_widget.layout().addWidget(layer_label)
        layer_widget.layout().addWidget(self._image_layers)
        self.layout().addWidget(layer_widget)

        # Select algorithm
        algo_widget = QWidget()
        algo_widget.setLayout(QHBoxLayout())
        algo_label = QLabel('Segmentation algorithm')
        self._algorithm = QComboBox()
        self._algorithm.addItems(['Threshold', 'Otsu', 'Cellpose'])
        self._algorithm.activated.connect(self._update_parameters)
        algo_widget.layout().addWidget(algo_label)
        algo_widget.layout().addWidget(self._algorithm)
        self.layout().addWidget(algo_widget)

        # Threshold parameter widget
        self.thresh_widget = QWidget()
        self.thresh_widget.setLayout(QHBoxLayout())
        thresh_label = QLabel('Threshold')
        thresh_slider = QSlider(Qt.Orientation.Horizontal,
                                minimum=0, maximum=100, value=20)
        thresh_slider.valueChanged.connect(self._update_thresh_val)
        self.thresh_val_label = QLabel('0.2')
        self.thresh_widget.layout().addWidget(thresh_label)
        self.thresh_widget.layout().addWidget(thresh_slider)
        self.thresh_widget.layout().addWidget(self.thresh_val_label)
        self.layout().addWidget(self.thresh_widget)

        # nbins parameter widget
        self.nbins_widget = QWidget()
        self.nbins_widget.setLayout(QHBoxLayout())
        nbins_label = QLabel('Number of bins')
        self.nbins_spinbox = QSpinBox(minimum=1, maximum=256, value=256)
        self.nbins_widget.layout().addWidget(nbins_label)
        self.nbins_widget.layout().addWidget(self.nbins_spinbox)
        self.layout().addWidget(self.nbins_widget)

        # use_gpu parameter widget
        self.gpu_widget = QWidget()
        self.gpu_widget.setLayout(QHBoxLayout())
        gpu_label = QLabel('Use GPU')
        self.gpu_checkbox = QCheckBox()
        self.gpu_checkbox.setChecked(True)
        self.gpu_widget.layout().addWidget(gpu_label)
        self.gpu_widget.layout().addWidget(self.gpu_checkbox)
        self.layout().addWidget(self.gpu_widget)

        # Run plugin
        run_btn = QPushButton('Segment')
        run_btn.clicked.connect(self._run_segmentation)
        self.layout().addWidget(run_btn)

        self._update_combo_box()
        self._update_parameters(0)

    def _update_thresh_val(self, val):
        self.thresh_val_label.setText(f'{val / 100}')

    def _update_parameters(self, index):
        algorithm = self._algorithm.itemText(index)

        if algorithm == 'Threshold':
            self.thresh_widget.setVisible(True)
            self.nbins_widget.setVisible(False)
            self.gpu_widget.setVisible(False)

        elif algorithm == 'Otsu':
            self.thresh_widget.setVisible(False)
            self.nbins_widget.setVisible(True)
            self.gpu_widget.setVisible(False)

        elif algorithm == 'Cellpose':
            self.thresh_widget.setVisible(False)
            self.nbins_widget.setVisible(False)
            self.gpu_widget.setVisible(True)

    def _update_combo_box(self):
        for layer_name in [self._image_layers.itemText(i) for i in range(self._image_layers.count())]:
            layer_name_index = self._image_layers.findText(layer_name)
            self._image_layers.removeItem(layer_name_index)

        for layer in [l for l in self.viewer.layers if isinstance(l, napari.layers.Image)]:
            if layer.name not in [self._image_layers.itemText(i) for i in range(self._image_layers.count())]:
                self._image_layers.addItem(layer.name)

    def _get_selected_image_layer(self):
        return self.viewer.layers[self._image_layers.currentText()]

    def _run_segmentation(self):
        input_img = self._get_selected_image_layer()
        algorithm = self._algorithm.currentText()
        threshold = float(self.thresh_val_label.text())
        nbins = self.nbins_spinbox.value()
        use_gpu = self.gpu_checkbox.isChecked()

        labels = segment_image(input_img=input_img,
                               algorithm=algorithm,
                               threshold=threshold,
                               nbins=nbins,
                               use_gpu=use_gpu)

        self.viewer.add_layer(labels)


viewer = napari.view_image(nuclei_img)
widget = SegmentImage(napari_viewer=viewer)
viewer.window.add_dock_widget(widget)
napari.utils.nbscreenshot(viewer)
