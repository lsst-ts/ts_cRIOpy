from lsst.ts.cRIOpy.M1M3FATable import (
    FATABLE_XINDEX,
    FATABLE_YINDEX,
    FATABLE_ZINDEX,
    FATABLE_SINDEX,
)

from .ActuatorsDisplay import Scales

__all__ = ["Topics", "TopicData", "TopicField"]


class TopicData:
    """
    Helper class. Used together with TopicField to construct topics.
    """

    def __init__(self, name, fields, topic, isEvent=True):
        self.name = name
        self.fields = fields
        self.selectedField = 0
        self.topic = topic
        self.isEvent = isEvent

    def getTopic(self):
        if self.isEvent:
            return "evt_" + self.topic
        return "tel_" + self.topic


class TopicField:
    def __init__(self, name, value, valueIndex, scale=Scales.GAUGE):
        self.name = name
        self.value = value
        self.valueIndex = valueIndex
        self.scale = scale

    def getValue(self, data):
        return getattr(data, self.value)


class OnOffField(TopicField):
    def __init__(self, name, value, valueIndex):
        super().__init__(name, value, valueIndex, Scales.ONOFF)


class WarningField(TopicField):
    def __init__(self, name, value, valueIndex):
        super().__init__(name, value, valueIndex, Scales.WARNING)


class BumpTestField(TopicField):
    def __init__(self, name, value, valueIndex):
        super().__init__(name, value, valueIndex, Scales.BUMP_TEST)


class EnabledDisabledField(TopicField):
    def __init__(self, name, value, valueIndex):
        super().__init__(name, value, valueIndex, Scales.ENABLED_DISABLED)


class Topics:
    """
    Class constructing list of all available topics.
    """

    def __init__(self):
        self.lastIndex = None

        self.topics = [
            TopicData(
                "FA Cylinder Pressures",
                [
                    TopicField(
                        "Primary Cylinders Push",
                        "primaryCylinderPushPressures",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Primary Cylinders Pull",
                        "primaryCylinderPullPressures",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Cylinder Push",
                        "secondaryCylinderPushPressures",
                        FATABLE_SINDEX,
                    ),
                    TopicField(
                        "Secondary Cylinder Pull",
                        "secondaryCylinderPullPressures",
                        FATABLE_SINDEX,
                    ),
                ],
                "forceActuatorPressure",
                False,
            ),
            TopicData(
                "Applied Aberration Forces",
                [TopicField("Z Forces", "zForces", FATABLE_ZINDEX)],
                "appliedAberrationForces",
            ),
            TopicData(
                "Applied Acceleration Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedAccelerationForces",
            ),
            TopicData(
                "Applied Active Optic Forces",
                [TopicField("Z Forces", "zForces", FATABLE_ZINDEX)],
                "appliedActiveOpticForces",
            ),
            TopicData(
                "Applied Azimuth Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedAzimuthForces",
            ),
            TopicData(
                "Applied Balance Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedBalanceForces",
            ),
            TopicData(
                "Applied Cylinder Forces",
                [
                    TopicField(
                        "Primary Cylinder Forces",
                        "primaryCylinderForces",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Cylinder Forces",
                        "secondaryCylinderForces",
                        FATABLE_SINDEX,
                    ),
                ],
                "appliedCylinderForces",
            ),
            TopicData(
                "Applied Elevation Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedElevationForces",
            ),
            TopicData(
                "Applied Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedForces",
            ),
            TopicData(
                "Applied Offset Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedOffsetForces",
            ),
            TopicData(
                "Applied Static Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedStaticForces",
            ),
            TopicData(
                "Applied Thermal Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedThermalForces",
            ),
            TopicData(
                "Applied Velocity Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "appliedVelocityForces",
            ),
            TopicData(
                "Pre-clipped Aberration Forces",
                [TopicField("Z Forces", "zForces", FATABLE_ZINDEX)],
                "preclippedAberrationForces",
            ),
            TopicData(
                "Pre-clipped Acceleration Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedAccelerationForces",
            ),
            TopicData(
                "Pre-clipped Active Optic Forces",
                [TopicField("Z Forces", "zForces", FATABLE_ZINDEX)],
                "preclippedActiveOpticForces",
            ),
            TopicData(
                "Pre-clipped Azimuth Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedAzimuthForces",
            ),
            TopicData(
                "Pre-clipped Balance Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedBalanceForces",
            ),
            TopicData(
                "Pre-clipped Cylinder Forces",
                [
                    TopicField(
                        "Primary Cylinder Forces",
                        "primaryCylinderForces",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Cylinder Forces",
                        "secondaryCylinderForces",
                        FATABLE_SINDEX,
                    ),
                ],
                "preclippedCylinderForces",
            ),
            TopicData(
                "Pre-clipped Elevation Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedElevationForces",
            ),
            TopicData(
                "Pre-clipped Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedForces",
            ),
            TopicData(
                "Pre-clipped Offset Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedOffsetForces",
            ),
            TopicData(
                "Pre-clipped Static Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedStaticForces",
            ),
            TopicData(
                "Pre-clipped Thermal Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedThermalForces",
            ),
            TopicData(
                "Pre-clipped Velocity Forces",
                [
                    TopicField("Z Forces", "zForces", FATABLE_ZINDEX),
                    TopicField("Y Forces", "yForces", FATABLE_YINDEX),
                    TopicField("X Forces", "xForces", FATABLE_XINDEX),
                ],
                "preclippedVelocityForces",
            ),
            TopicData(
                "Measured forces",
                [
                    TopicField(
                        "Primary Cylinder Forces",
                        "primaryCylinderForce",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Cylinder Forces",
                        "secondaryCylinderForce",
                        FATABLE_SINDEX,
                    ),
                    TopicField(
                        "Z Forces",
                        "zForce",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Y Forces",
                        "yForce",
                        FATABLE_YINDEX,
                    ),
                    TopicField(
                        "X Forces",
                        "xForce",
                        FATABLE_XINDEX,
                    ),
                ],
                "forceActuatorData",
                False,
            ),
            TopicData(
                "Force Actuator ILC Info",
                [
                    TopicField("Subnet", "modbusSubnet", FATABLE_ZINDEX),
                    TopicField("Address", "modbusAddress", FATABLE_ZINDEX),
                    TopicField(
                        "Major Revision",
                        "majorRevision",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Minor Revision",
                        "minorRevision",
                        FATABLE_ZINDEX,
                    ),
                    TopicField("ADC Scan Rate", "adcScanRate", FATABLE_ZINDEX),
                ],
                "forceActuatorInfo",
            ),
            TopicData(
                "Force Actuator Id Info",
                [
                    TopicField(
                        "X Data Reference Id",
                        "xDataReferenceId",
                        FATABLE_XINDEX,
                    ),
                    TopicField(
                        "Y Data Reference Id",
                        "yDataReferenceId",
                        FATABLE_YINDEX,
                    ),
                    TopicField(
                        "Z Data Reference Id",
                        "zDataReferenceId",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "S Data Reference Id",
                        "sDataReferenceId",
                        FATABLE_SINDEX,
                    ),
                    TopicField("ILC Unique Id", "ilcUniqueId", FATABLE_ZINDEX),
                    TopicField(
                        "Mezzanine Unique Id",
                        "xDataReferenceId",
                        FATABLE_ZINDEX,
                    ),
                ],
                "forceActuatorInfo",
            ),
            TopicData(
                "Force Actuator Settings",
                [
                    EnabledDisabledField(
                        "Enabled/Disabled", "enabledActuators", FATABLE_ZINDEX
                    ),
                ],
                "forceActuatorSettings",
            ),
            TopicData(
                "Force Actuator Main Calibration Info",
                [
                    TopicField(
                        "Primary Coefficient",
                        "mainPrimaryCylinderCoefficient",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Primary Offset",
                        "mainPrimaryCylinderLoadCellOffset",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Primary Sensitivity",
                        "mainPrimaryCylinderLoadCellSensitivity",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Coefficient",
                        "mainSecondaryCylinderCoefficient",
                        FATABLE_SINDEX,
                    ),
                    TopicField(
                        "Secondary Offset",
                        "mainSecondaryCylinderLoadCellOffset",
                        FATABLE_SINDEX,
                    ),
                    TopicField(
                        "Secondary Sensitivity",
                        "mainSecondaryLoadCellSensitivity",
                        FATABLE_SINDEX,
                    ),
                ],
                "forceActuatorInfo",
            ),
            TopicData(
                "Force Actuator Backup Calibration Info",
                [
                    TopicField(
                        "Primary Coefficient",
                        "backupPrimaryCylinderCoefficient",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Primary Offset",
                        "backupPrimaryCylinderLoadCellOffset",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Primary Sensitivity",
                        "backupPrimaryCylinderLoadCellSensitivity",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Coefficient",
                        "backupSecondaryCylinderCoefficient",
                        FATABLE_SINDEX,
                    ),
                    TopicField(
                        "Secondary Offset",
                        "backupSecondaryCylinderLoadCellOffset",
                        FATABLE_SINDEX,
                    ),
                    TopicField(
                        "Secondary Sensitivity",
                        "backupSecondaryLoadCellSensitivity",
                        FATABLE_SINDEX,
                    ),
                ],
                "forceActuatorInfo",
            ),
            TopicData(
                "Force Actuator Mezzanine Calibration Info",
                [
                    TopicField(
                        "Primary Cylinder Gain",
                        "mezzaninePrimaryCylinderGain",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Cylinder Gain",
                        "mezzanineSecondaryCylinderGain",
                        FATABLE_SINDEX,
                    ),
                ],
                "forceActuatorInfo",
            ),
            TopicData(
                "Force Actuator Position Info",
                [
                    TopicField(
                        "Actuator Type",
                        "actuatorType",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Actuator Orientation",
                        "actuatorOrientation",
                        FATABLE_ZINDEX,
                    ),
                    TopicField("X Position", "xPosition", FATABLE_ZINDEX),
                    TopicField("Y Position", "yPosition", FATABLE_ZINDEX),
                    TopicField("Z Position", "zPosition", FATABLE_ZINDEX),
                ],
                "forceActuatorInfo",
            ),
            TopicData(
                "Force Actuator State",
                [TopicField("ILC State", "ilcState", FATABLE_ZINDEX)],
                "forceActuatorState",
            ),
            TopicData(
                "Force Actuator Warning",
                [
                    WarningField("Major Fault", "majorFault", FATABLE_ZINDEX),
                    WarningField("Minor Fault", "minorFault", FATABLE_ZINDEX),
                    WarningField(
                        "Fault Override",
                        "faultOverride",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Main Calibration Error",
                        "mainCalibrationError",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Backup Calibration Error",
                        "backupCalibrationError",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Error",
                        "mezzanineError",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Bootloader Active",
                        "mezzanineBootloaderActive",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Unique Id CRC Error",
                        "uniqueIdCRCError",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Application Type Mismatch",
                        "applicationTypeMismatch",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Application Missing",
                        "applicationMissing",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "OneWire Mismatch",
                        "oneWireMissing",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "OneWire1 Mismatch",
                        "oneWire1Mismatch",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "OnewWire2 Mismatch",
                        "oneWire2Mismatch",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Watchdog Reset",
                        "watchdogReset",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Brownout",
                        "brownOut",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Event Trap Reset",
                        "eventTrapReset",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "SSR Power Fault",
                        "ssrPowerFault",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "AUX Power Fault",
                        "auxPowerFault",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Power Fault",
                        "mezzaninePowerFault",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Current Ampl Fault",
                        "mezzanineCurrentAmp1Fault",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Current Amp2 Fault",
                        "mezzanineCurrentAmp2Fault",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Unique ID CRC Error",
                        "mezzanineUniqueIdCRCError",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Main Calibration Error",
                        "mezzanineMainCalibrationError",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Backup Calibration Error",
                        "mezzanineBackupCalibrationError",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Event Trap Reset",
                        "mezzanineEventTrapReset",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Application Missing",
                        "mezzanineApplicationMissing",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Mezzanine Application CRC Mismatch",
                        "mezzanineApplicationCRCMismatch",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "ILC Fault",
                        "ilcFault",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Broadcast Counter Warning",
                        "broadcastCounterWarning",
                        FATABLE_ZINDEX,
                    ),
                ],
                "forceActuatorWarning",
            ),
            TopicData(
                "Force Actuator Force Warning",
                [
                    WarningField(
                        "Primary Axis Measured Force Warning",
                        "primaryAxisMeasuredForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Secondary Axis Measured Force Warning",
                        "secondaryAxisMeasuredForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Primary Axis Following Error Warning",
                        "primaryAxisFollowingErrorWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Secondary Axis Following Error Warning",
                        "secondaryAxisFollowingErrorWarning",
                        FATABLE_ZINDEX,
                    ),
                ],
                "forceActuatorForceWarning",
            ),
            TopicData(
                "FA Setpoint Warning",
                [
                    WarningField(
                        "Safety limit",
                        "safetyLimitWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Near neighbor",
                        "nearNeighborWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Far neighbor",
                        "farNeighborWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Elevation force",
                        "elevationForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Azimuth force",
                        "azimuthForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Thermal force",
                        "thermalForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Balance force",
                        "balanceForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Acceleration force",
                        "accelerationForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Active optic",
                        "activeOpticForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Static force",
                        "staticForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Aberration force",
                        "aberrationForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Offset force",
                        "offsetForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Velocity force",
                        "velocityForceWarning",
                        FATABLE_ZINDEX,
                    ),
                    WarningField(
                        "Force setpoint",
                        "forceWarning",
                        FATABLE_ZINDEX,
                    ),
                ],
                "forceSetpointWarning",
            ),
            TopicData(
                "FA Bump Test",
                [
                    BumpTestField("Primary Test", "primaryTest", FATABLE_ZINDEX),
                    BumpTestField(
                        "Secondary Test",
                        "secondaryTest",
                        FATABLE_SINDEX,
                    ),
                    TopicField(
                        "Primary Timestamps",
                        "primaryTestTimestamps",
                        FATABLE_ZINDEX,
                    ),
                    TopicField(
                        "Secondary Timestamps",
                        "secondaryTestTimestamps",
                        FATABLE_SINDEX,
                    ),
                ],
                "forceActuatorBumpTestStatus",
            ),
            TopicData(
                "FA enabled",
                [
                    EnabledDisabledField(
                        "Enabled FAs",
                        "forceActuatorEnabled",
                        FATABLE_ZINDEX,
                    ),
                ],
                "enabledForceActuators",
            ),
        ]

    def changeTopic(self, index, slot, comm):
        if self.lastIndex is not None:
            getattr(comm, self.topics[self.lastIndex].topic).disconnect(slot)

        self.lastIndex = index
        if index is None:
            return

        getattr(comm, self.topics[index].topic).connect(slot)
