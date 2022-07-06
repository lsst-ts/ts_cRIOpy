# This file is part of M1M3 SS GUI.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org). See the COPYRIGHT file at the top - level directory
# of this distribution for details of code ownership.
#
# This program is free software : you can redistribute it and / or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.If not, see <https://www.gnu.org/licenses/>.

import copy

import astropy.units as u
from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QApplication,
)
from PySide2.QtCore import Signal, Slot
from asyncqt import asyncSlot

from lsst.ts.idl.enums.MTM1M3 import DetailedState, HardpointActuatorMotionStates

from ..GUI import Force, Moment, Mm, UnitLabel, OnOffLabel
from ..GUI.SAL import DetailedStateEnabledButton, SALCommand


class OffsetsTypeButton(QPushButton):
    """Button to change units of offset movement. Knows how to convert value from selected units into steps.

    Attributes
    ----------
    unitChanged : Signal(float, float, str, int)
        Signal emmited after unit changes. Parameters passed is old and new
        scale, unit name and number of decimal values to shown.
    """

    unitChanged = Signal(float, float, str, int)

    def __init__(self):
        super().__init__()

        # member array is unit name, scale factor, numbe of decimals, unit
        # abbrevation
        self._units = [
            ["&Motor steps", 1, 0, "motor"],
            ["&Encoder steps", 1, 0, "encoder"],
            ["&Displacement (um)", 1, 1, "um"],
            ["&Displacement (mm)", 1, 4, "mm"],
        ]
        self.setToolTip("Click to change move units")
        self.setScales(0.0607, 0.2442)

        self._selectedIndex = 0
        self.setSelectedIndex(0)
        self.clicked.connect(self._clicked)

    def setSelectedIndex(self, index):
        """Sets new selected index.

        Parameters
        ----------
        index : int
            New index to set.
        """
        oldScale = self.getScale()

        self._selectedIndex = index
        self.setText(self._units[index][0])

        self.unitChanged.emit(
            oldScale, self.getScale(), self.getUnit(), self.getDecimals()
        )

    def getScale(self):
        """Returns scale used.

        Returns
        -------
        scale : float
            Scale factor for the current unit.
        """
        return self._units[self._selectedIndex][1]

    def getDecimals(self):
        """Returns number of decimals suggested for display. 0 for integer values."""
        return self._units[self._selectedIndex][2]

    def getUnit(self):
        return self._units[self._selectedIndex][3]

    def setScales(self, micrometersPerStep, micrometersPerEncoder):
        self._units[1][1] = micrometersPerEncoder / micrometersPerStep
        self._units[2][1] = 1.0 / micrometersPerStep
        self._units[3][1] = u.mm.to(u.um) / micrometersPerStep

    @Slot(bool)
    def _clicked(self, checked):
        newIndex = self._selectedIndex + 1
        if newIndex >= len(self._units):
            newIndex = 0
        self.setSelectedIndex(newIndex)

    def getSteps(self, value):
        return int(value * self.getScale())


class HardpointsWidget(QWidget):
    """Displays hardpoint data - encoders and calculated position, hardpoint
    state, and M1M3 displacement."""

    def __init__(self, m1m3):
        super().__init__()
        self.m1m3 = m1m3

        layout = QVBoxLayout()

        self.dataLayout = QGridLayout()

        layout.addLayout(self.dataLayout)
        self.setLayout(layout)

        self.dataLayout.addWidget(QLabel("<b>Hardpoint</b>"), 0, 0)
        for hp in range(1, 7):
            self.dataLayout.addWidget(QLabel(f"<b>{hp}</b>"), 0, hp)

        self.variables = {
            "stepsQueued": ("Steps queued", UnitLabel()),
            "stepsCommanded": ("Steps commanded", UnitLabel()),
            "encoder": ("Encoder", UnitLabel()),
            "measuredForce": ("Measured force", Force(".03f")),
            "displacement": ("Displacement", Mm()),
        }

        row = 1

        def addRow(textValue, row):
            ret = []
            self.dataLayout.addWidget(QLabel(textValue[0]), row, 0)
            for hp in range(6):
                label = copy.copy(textValue[1])
                self.dataLayout.addWidget(label, row, 1 + hp)
                ret.append(label)
            return ret

        for k, v in self.variables.items():
            setattr(self, k, addRow(v, row))
            row += 1

        self.lastEditedSteps = [0] * 6

        self.offsetType = OffsetsTypeButton()
        self.offsetType.unitChanged.connect(self._HPUnitChanged)

        self.dataLayout.addWidget(self.offsetType, row, 0)
        self._hpMoveRow = row
        self._HPUnitChanged(1, 1, " motor", 0)
        row += 1

        enabledStates = [
            DetailedState.PARKEDENGINEERING,
            DetailedState.RAISINGENGINEERING,
            DetailedState.ACTIVEENGINEERING,
            DetailedState.LOWERINGENGINEERING,
        ]

        self._lastOffsetFocused = None

        copyHPButton = QPushButton("Copy")
        copyHPButton.setToolTip("Use last edited (focused) value for all HP offsets")
        copyHPButton.clicked.connect(self._copyHP)
        self.dataLayout.addWidget(copyHPButton, row, 0)

        moveHPButton = DetailedStateEnabledButton("Move", m1m3, enabledStates)
        moveHPButton.clicked.connect(self._moveHP)
        self.dataLayout.addWidget(moveHPButton, row, 1, 1, 2)

        stopHPButton = DetailedStateEnabledButton("Stop", m1m3, enabledStates)
        stopHPButton.clicked.connect(self._stopHP)
        self.dataLayout.addWidget(stopHPButton, row, 3, 1, 2)

        reset = QPushButton("Reset")
        reset.clicked.connect(self._reset)
        self.dataLayout.addWidget(reset, row, 5, 1, 2)

        row += 1

        self.monitorData = {
            "breakawayLVDT": ("Breakaway LVDT", UnitLabel(".02f")),
            "displacementLVDT": ("Displacement LVDT", UnitLabel(".02f")),
            "breakawayPressure": ("Breakaway Pressure", UnitLabel(".02f")),
            "pressureSensor1": ("Pressure Sensor 1", UnitLabel(".04f")),
            "pressureSensor2": ("Pressure Sensor 2", UnitLabel(".04f")),
            "pressureSensor3": ("Pressure Sensor 3", UnitLabel(".04f")),
        }

        for k, v in self.monitorData.items():
            setattr(self, k, addRow(v, row))
            row += 1

        self.warnings = {
            "majorFault": ("Major fault", OnOffLabel()),
            "minorFault": ("Minor fault", OnOffLabel()),
            "faultOverride": ("Fault override", OnOffLabel()),
            "mainCalibrationError": ("Main calibration error", OnOffLabel()),
            "backupCalibrationError": ("Backup calibration error", OnOffLabel()),
            "limitSwitch1Operated": ("Limit switch 1", OnOffLabel()),
            "limitSwitch2Operated": ("Limit switch 2", OnOffLabel()),
        }

        for k, v in self.warnings.items():
            setattr(self, k, addRow(v, row))
            row += 1

        self.dataLayout.addWidget(QLabel("Motion state"), row, 0)
        self.hpStates = []
        for hp in range(6):
            self.hpStates.append(QLabel())
            self.dataLayout.addWidget(self.hpStates[hp], row, hp + 1)
        row += 1

        self.forces = {
            "forceMagnitude": ("Total force", Force()),
            "fx": ("Force X", Force()),
            "fy": ("Force Y", Force()),
            "fz": ("Force Z", Force()),
            "mx": ("Moment X", Moment()),
            "my": ("Moment Y", Moment()),
            "mz": ("Moment Z", Moment()),
        }

        self.dataLayout.addWidget(QLabel(), row, 0)
        row += 1

        def addDataRow(variables, row, col=0):
            for k, v in variables.items():
                self.dataLayout.addWidget(QLabel(f"<b>{v[0]}</b>"), row, col)
                setattr(self, k, v[1])
                self.dataLayout.addWidget(v[1], row + 1, col)
                col += 1

        addDataRow(self.forces, row)
        row += 2
        self.dataLayout.addWidget(QLabel(), row, 0)
        row += 1
        self.positions = {
            "xPosition": ("Position X", Mm()),
            "yPosition": ("Position Y", Mm()),
            "zPosition": ("Position Z", Mm()),
            "xRotation": ("Rotation X", Mm()),
            "yRotation": ("Rotation Y", Mm()),
            "zRotation": ("Rotation Z", Mm()),
        }
        addDataRow(self.positions, row, 1)

        layout.addStretch()

        QApplication.instance().focusChanged.connect(self.focusChanged)

        self.m1m3.hardpointActuatorSettings.connect(self.hardpointActuatorSettings)

        self.m1m3.hardpointActuatorData.connect(self.hardpointActuatorData)
        self.m1m3.hardpointActuatorState.connect(self.hardpointActuatorState)
        self.m1m3.hardpointMonitorData.connect(self.hardpointMonitorData)
        self.m1m3.hardpointActuatorWarning.connect(self.hardpointActuatorWarning)

    @Slot(QWidget, QWidget)
    def focusChanged(self, old, new):
        for hp in range(len(self.hpOffsets)):
            if self.hpOffsets[hp] == old:
                self.lastEditedSteps[hp] = self.offsetType.getScale() * old.value()
                self._lastOffsetFocused = hp
                return

    @Slot(float, float, str, int)
    def _HPUnitChanged(self, oldScale, newScale, units, decimals):
        self.hpOffsets = []
        for hp in range(6):
            if decimals == 0:
                sb = QSpinBox()
                maxSteps = 70000 * 4.03 / self.offsetType.getSteps(1)
                sb.setRange(-maxSteps, maxSteps)
                sb.setSingleStep(100)
            else:
                sb = QDoubleSpinBox()
                maxRange = 15 * (10 ** (4 - decimals))
                sb.setRange(-maxRange, maxRange)
                sb.setDecimals(decimals)
                sb.setSingleStep(1)

            sb.setSuffix(" " + units)
            self.dataLayout.addWidget(sb, self._hpMoveRow, 1 + hp)
            if self.lastEditedSteps is not None:
                sb.setValue(self.lastEditedSteps[hp] / self.offsetType.getScale())

            self.hpOffsets.append(sb)

    @Slot()
    def _copyHP(self):
        if self._lastOffsetFocused:
            v = self.hpOffsets[self._lastOffsetFocused].value()
            for offset in self.hpOffsets:
                offset.setValue(v)
            self.lastEditedSteps = [self.offsetType.getScale() * v] * 6

    @SALCommand
    def _moveIt(self, **kvargs):
        return self.m1m3.remote.cmd_moveHardpointActuators

    @asyncSlot()
    async def _moveHP(self):
        steps = list(map(lambda x: self.offsetType.getSteps(x.value()), self.hpOffsets))
        await self._moveIt(steps=steps)

    @SALCommand
    def _stopIt(self, **kvargs):
        return self.m1m3.remote.cmd_stopHardpointMotion

    @asyncSlot()
    async def _stopHP(self):
        await self._stopIt()

    @Slot()
    def _reset(self):
        for hp in range(6):
            self.hpOffsets[hp].setValue(0)

    def _fillRow(self, hpData, rowLabels):
        for hp in range(6):
            rowLabels[hp].setValue(hpData[hp])

    @Slot(map)
    def hardpointActuatorSettings(self, data):
        self.offsetType.setScales(data.micrometersPerStep, data.micrometersPerEncoder)

    @Slot(map)
    def hardpointActuatorData(self, data):
        for k, v in self.variables.items():
            self._fillRow(getattr(data, k), getattr(self, k))

        for k, v in self.forces.items():
            getattr(self, k).setValue(getattr(data, k))

        for k, v in self.positions.items():
            getattr(self, k).setValue(getattr(data, k))

    @Slot(map)
    def hardpointActuatorState(self, data):
        states = {
            HardpointActuatorMotionStates.STANDBY: "Standby",
            HardpointActuatorMotionStates.CHASING: "Chasing",
            HardpointActuatorMotionStates.STEPPING: "Stepping",
            HardpointActuatorMotionStates.QUICKPOSITIONING: "Quick positioning",
            HardpointActuatorMotionStates.FINEPOSITIONING: "Fine positioning",
        }

        def getHpState(state):
            try:
                return states[state]
            except KeyError:
                return f"Invalid {state}"

        for hp in range(6):
            self.hpStates[hp].setText(getHpState(data.motionState[hp]))

    @Slot(map)
    def hardpointMonitorData(self, data):
        for k, v in self.monitorData.items():
            self._fillRow(getattr(data, k), getattr(self, k))

    @Slot(map)
    def hardpointActuatorWarning(self, data):
        for k, v in self.warnings.items():
            self._fillRow(getattr(data, k), getattr(self, k))