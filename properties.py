from qtpy.QtWidgets import QCheckBox, QVBoxLayout, QWidget


class Properties(QWidget):
    def __init__(self, napari_viewer="napari.viewer.Viewer()", container=None):
        super().__init__()

        self.setLayout(QVBoxLayout())

        self.props = [
            "area",
            "area_bbox",
            "area_convex",
            "area_filled",
            "axis_major_length",
            "axis_minor_length",
            "bboxtuple",
            "centroidarray",
            # "centroid_localarray",
            # "centroid_weightedarray",
            # "centroid_weighted_localarray",
            # "coords_scaled",
            # "coords",
            # "eccentricity",
            # "equivalent_diameter_area",
            # "euler_numberint",
            # "extent",
            # "feret_diameter_max",
            # "image",
            # "image_convex",
            # "image_filled",
            # "image_intensity",
            # "inertia_tensor",
            # "inertia_tensor_eigvalstuple",
            # "intensity_max",
            # "intensity_mean",
            # "intensity_min",
            # "intensity_std",
            # "labelint",
            # "moments",
            # "m_ij",
            # "moments_central",
            # "mu_ij",
            # "moments_hutuple",
            # "moments_normalized",
            # "nu_ij",
            # "moments_weighted",
            # "wm_ij",
            # "moments_weighted_central",
            # "wmu_ij",
            # "moments_weighted_hutuple",
            # "moments_weighted_normalized",
            # "wnu_ij",
            # "num_pixelsint",
            # "orientation",
            # "perimeter",
            # "perimeter_crofton",
            # "slicetuple",
            # "solidity",
        ]
        self.checkboxes = []
        for prop in self.props:
            self.checkboxes.append(QCheckBox(prop))
            if container is not None:
                self.checkboxes[-1].toggled.connect(
                    container.main_widget._run_segmentation
                )

        for checkbox in self.checkboxes:
            self.layout().addWidget(checkbox)

    def get_properties(self):
        checked_props = []
        for checkbox in self.checkboxes:
            if checkbox.checkState():
                checked_props.append(checkbox.text())
        return checked_props
