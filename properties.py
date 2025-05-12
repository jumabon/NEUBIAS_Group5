from qtpy.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QCheckBox


class Properties(QWidget):
    def __init__(self, napari_viewer="napari.viewer.Viewer()", container=None):
        super().__init__()

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.props = [
            "area", "area_bbox", "area_convex", "area_filled",
            "axis_major_length", "axis_minor_length", "bboxtuple", "centroidarray",
            "centroid_localarray", "centroid_weightedarray", "centroid_weighted_localarray",
            "coords_scaled", "coords", "eccentricity", "equivalent_diameter_area",
            "euler_numberint", "extent", "feret_diameter_max", "image", "image_convex",
            "image_filled", "image_intensity", "inertia_tensor", "inertia_tensor_eigvalstuple",
            "intensity_max", "intensity_mean", "intensity_min", "intensity_std", "labelint",
            "moments", "m_ij", "moments_central", "mu_ij", "moments_hutuple",
            "moments_normalized", "nu_ij", "moments_weighted", "wm_ij",
            "moments_weighted_central", "wmu_ij", "moments_weighted_hutuple",
            "moments_weighted_normalized", "wnu_ij", "num_pixelsint", "orientation",
            "perimeter", "perimeter_crofton", "slicetuple", "solidity"
        ]

        self.checkboxes = []
        for prop in self.props:
            checkbox = QCheckBox(prop)
            self.checkboxes.append(checkbox)
            if container is not None:
                checkbox.toggled.connect(container.main_widget._run_segmentation)
            scroll_layout.addWidget(checkbox)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)

        main_layout.addWidget(scroll)

    def get_properties(self):
        return [cb.text() for cb in self.checkboxes if cb.checkState()]
