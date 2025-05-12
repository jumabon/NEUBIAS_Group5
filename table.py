from qtpy.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Table(QWidget):
    def __init__(self, napari_viewer="napari.viewer.Viewer()", container=None):
        super().__init__()

        self.setLayout(QVBoxLayout())

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.layout().addWidget(self.table)

    def _update_table(self, region_props_dict):
        # num_cols must be integer
        num_cols = len(region_props_dict)
        self.table.setColumnCount(num_cols)

        # Headers must be a list of strings
        header_list = list(region_props_dict.keys())
        self.table.setHorizontalHeaderLabels(header_list)

        num_rows = len(region_props_dict[header_list[0]])
        for num_row in range(num_rows):
            self.table.insertRow(self.table.rowCount())

        for col, key in enumerate(header_list):
            for row, value in enumerate(region_props_dict[key]):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
