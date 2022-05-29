# This file is part of cRIO generic GUI.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https: //www.lsst.org).
# See the COPYRIGHT file at the top - level directory of this distribution
# for details of code ownership.
#
# This program is free software : you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.If not, see < https:  // www.gnu.org/licenses/>.

from PySide2.QtWidgets import QFormLayout, QWidget

__all__ = ["DataFormWidget"]


class DataFormWidget(QWidget):
    """
    Creates labels with data displays. Update fields on signal with new values.

    Parameters
    ----------
    signal : `QSignal`
        Signal with new data. It is assumed DataLabel childs passed in fields
        contain DataLabel with field corresponding to fields in the signal.

    fields : `[(str, DataLabel)]`
        Tuple of text and label. Label shall be child of DataLabel with
        fieldname set.

    Usage
    -----
       myWidget = DataFormWidget(sal.errors, [("Power", WarningLabel(None, "state"))])
    """

    def __init__(self, signal, fields):
        super().__init__()

        layout = QFormLayout()
        for (text, label) in fields:
            layout.addRow(text, label)
        self.setLayout(layout)

        signal.connect(self._process_signal)

    def _process_signal(self, data):
        for e in dir(data):
            ch = self.findChild(QWidget, e)
            if ch is not None:
                ch.setValue(getattr(data, e))
