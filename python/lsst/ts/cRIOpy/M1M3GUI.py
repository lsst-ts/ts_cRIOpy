#!/usr/bin/env python3.8
# -'''- coding: utf-8 -'''-

from lsst.ts.cRIOpy.GUI import (
    Application,
    ApplicationControlWidget,
    ActuatorOverviewPageWidget,
    AirPageWidget,
    CellLightPageWidget,
    CompressorsPageWidget,
    DCAccelerometerPageWidget,
    EnabledForceActuators,
    ForceActuatorGraphPageWidget,
    ForceActuatorValuePageWidget,
    ForceBalanceSystemPageWidget,
    ForceActuatorBumpTestPageWidget,
    GyroPageWidget,
    HardpointsWidget,
    IMSPageWidget,
    InclinometerPageWidget,
    InterlockPageWidget,
    OffsetsWidget,
    OverviewPageWidget,
    PIDPageWidget,
    PowerPageWidget,
    SALLog,
    SALErrorCodeWidget,
    SALStatusBar,
)

from lsst.ts.cRIOpy.GUI.M1M3GUI import detailedStateString

from PySide2.QtCore import QSettings, Slot
from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QHBoxLayout,
    QListWidget,
    QTabWidget,
    QGroupBox,
)

from asyncqt import asyncClose
import asyncio


class EUI(QMainWindow):
    def __init__(self, m1m3, mtmount, compressor_1, compressor_2):
        super().__init__()
        self.m1m3 = m1m3
        self.mtmount = mtmount
        self.compressor_1 = compressor_1
        self.compressor_2 = compressor_2

        controlWidget = QGroupBox("Application Control")
        applicationControl = ApplicationControlWidget(self.m1m3)
        applicationControlLayout = QVBoxLayout()
        applicationControlLayout.addWidget(applicationControl)
        controlWidget.setLayout(applicationControlLayout)

        self.applicationPagination = QListWidget()
        self.applicationPagination.currentRowChanged.connect(self.changePage)

        self.tabWidget = QTabWidget()
        self.tabWidget.tabBar().hide()

        self.addPage("Overview", OverviewPageWidget(self.m1m3, self.mtmount))
        self.addPage("Actuator Overview", ActuatorOverviewPageWidget(self.m1m3))
        self.addPage("Hardpoints", HardpointsWidget(self.m1m3))
        self.addPage("Offsets", OffsetsWidget(self.m1m3))
        self.addPage("DC Accelerometers", DCAccelerometerPageWidget(self.m1m3))
        self.addPage("Gyro", GyroPageWidget(self.m1m3))
        self.addPage("IMS", IMSPageWidget(self.m1m3))
        self.addPage("Inclinometer", InclinometerPageWidget(self.m1m3))
        self.addPage("Interlock", InterlockPageWidget(self.m1m3))
        self.addPage("Lights", CellLightPageWidget(self.m1m3))
        self.addPage("Air", AirPageWidget(self.m1m3))
        self.addPage("Power", PowerPageWidget(self.m1m3))
        self.addPage("PID", PIDPageWidget(self.m1m3))
        self.addPage("Force Balance System", ForceBalanceSystemPageWidget(self.m1m3))
        self.addPage(
            "Force Actuator Bump Test", ForceActuatorBumpTestPageWidget(self.m1m3)
        )
        self.addPage("Enabled Force Actuators", EnabledForceActuators(self.m1m3))
        self.addPage("Force Actuator Graph", ForceActuatorGraphPageWidget(self.m1m3))
        self.addPage("Force Actuator Value", ForceActuatorValuePageWidget(self.m1m3))
        self.addPage("Compressor 1", CompressorsPageWidget(self.compressor_1))
        self.addPage("Compressor 2", CompressorsPageWidget(self.compressor_2))
        self.addPage("SAL Log", SALLog.Widget(self.m1m3))
        self.addPage("SAL Errors", SALErrorCodeWidget(self.m1m3))

        self.applicationPagination.setCurrentRow(0)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(controlWidget)
        leftLayout.addWidget(self.applicationPagination)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addWidget(self.tabWidget)

        m1m3Widget = QWidget()
        m1m3Widget.setLayout(layout)

        self.setCentralWidget(m1m3Widget)
        self.setStatusBar(SALStatusBar([self.m1m3, self.mtmount], detailedStateString))

        self.setMinimumSize(700, 400)

        settings = QSettings("LSST.TS", "M1M3GUI")
        try:
            self.restoreGeometry(settings.value("geometry"))
            self.restoreState(settings.value("windowState"))
        except AttributeError:
            self.resize(1000, 700)

    def addPage(self, name, widget):
        self.applicationPagination.addItem(name)
        self.tabWidget.addTab(widget, name)

    @Slot(int)
    def changePage(self, row):
        if row < 0:
            return
        self.tabWidget.setCurrentIndex(row)

    @asyncClose
    async def closeEvent(self, event):
        settings = QSettings("LSST.TS", "M1M3GUI")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        await asyncio.gather(
            self.m1m3.close(),
            self.mtmount.close(),
            self.compressor_1.close(),
            self.compressor_2.close(),
        )
        super().closeEvent(event)


def run():
    # Create the Qt Application
    app = Application(EUI)
    app.addComm("MTM1M3")
    app.addComm(
        "MTMount", include=["azimuth", "elevation", "heartbeat", "simulationMode"]
    )
    app.addComm("MTAirCompressor", index=1)
    app.addComm("MTAirCompressor", index=2)

    app.run()
