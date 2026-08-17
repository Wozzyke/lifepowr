"""Constants for the LifePowr FlexiO integration."""

from __future__ import annotations

DOMAIN = "lifepowr"

MANUFACTURER = "LifePowr"
MODEL = "FlexiO"

DEFAULT_PORT = 80
WEBSOCKET_PATH = "/wsapp/"

CONF_HOST = "host"

# ----------------------------------------------------------------------
# Topics discovered from websocket reverse engineering
# ----------------------------------------------------------------------

TOPIC_DIAGNOSTICS_AWS = "diagnostics/aws"
TOPIC_DIAGNOSTICS_BMS = "diagnostics/bms"
TOPIC_DIAGNOSTICS_CONNECTED = "diagnostics/connected"
TOPIC_DIAGNOSTICS_EVDISCOVERY = "diagnostics/evDiscovery"
TOPIC_DIAGNOSTICS_INVERTER = "diagnostics/inverter"
TOPIC_DIAGNOSTICS_IOMANAGER = "diagnostics/iomanager"
TOPIC_DIAGNOSTICS_MODBUS = "diagnostics/modbus"
TOPIC_DIAGNOSTICS_P1 = "diagnostics/p1"
TOPIC_AWS_BROKER = "/flags/awsBrokerReady"

TOPIC_FCR = "iomanager/Publicationsq1/$aws/rules/aggregator"

TOPIC_AWS_FLEET_UPDATE = (
    "iomanager/aws/fleet/updates/[thingName]/individual"
)

# ----------------------------------------------------------------------
# Diagnostics entities
# ----------------------------------------------------------------------

DIAGNOSTIC_TOPICS = {
    "aws": TOPIC_DIAGNOSTICS_AWS,
    "bms": TOPIC_DIAGNOSTICS_BMS,
    "configured": None,
    "connected": TOPIC_DIAGNOSTICS_CONNECTED,
    "eastron": None,
    "ems": None,
    "ev": None,
    "ev_discovery": TOPIC_DIAGNOSTICS_EVDISCOVERY,
    "inverter": TOPIC_DIAGNOSTICS_INVERTER,
    "ioapi": None,
    "iodaemon": None,
    "iomanager": TOPIC_DIAGNOSTICS_IOMANAGER,
    "linked": None,
    "modbus": TOPIC_DIAGNOSTICS_MODBUS,
    "p1": TOPIC_DIAGNOSTICS_P1,
    "storage": None,
    "update": None,
}
# ----------------------------------------------------------------------
# FCR fields
# ----------------------------------------------------------------------

FCR_BASELINE = "frequencyResponseBaseline"

FCR_MEASUREMENT = "frequencyResponseMeasurement"

FCR_ERROR = "frequencyResponseError"

FCR_MARGIN_CHARGE = (
    "frequencyResponseAvailableMarginCharge"
)

FCR_MARGIN_DISCHARGE = (
    "frequencyResponseAvailableMarginDischarge"
)

FCR_RESPONSE_POWER = (
    "frequencyResponseChargeDischargePower"
)

# ----------------------------------------------------------------------
# Binary sensors
# ----------------------------------------------------------------------

BINARY_SENSORS = [
    {
        "key": "ems",
        "name": "EMS",
        "topic": "diagnostics/ems",
        "icon": "mdi:home-lightning-bolt",
    },
    {
        "key": "linked",
        "name": "Linked",
        "topic": "diagnostics/linked",
        "icon": "mdi:link-variant",
    },
    {
        "key": "aws_broker_ready",
        "name": "AWS Broker Ready",
        "topic": TOPIC_AWS_BROKER,
        "icon": "mdi:cloud-check",
    },
]

# ----------------------------------------------------------------------
# FCR Sensors
# ----------------------------------------------------------------------

FCR_SENSORS = [
    {
        "key": "fcr_baseline",
        "name": "FCR Baseline",
        "field": FCR_BASELINE,
        "icon": "mdi:sine-wave",
        "native_unit": None,
    },
    {
        "key": "fcr_measurement",
        "name": "FCR Measurement",
        "field": FCR_MEASUREMENT,
        "icon": "mdi:chart-line",
        "native_unit": None,
    },
    {
        "key": "fcr_error",
        "name": "FCR Error",
        "field": FCR_ERROR,
        "icon": "mdi:alert-outline",
        "native_unit": None,
    },
    {
        "key": "fcr_margin_charge",
        "name": "FCR Available Margin Charge",
        "field": FCR_MARGIN_CHARGE,
        "icon": "mdi:battery-plus",
        "native_unit": "kW",
    },
    {
        "key": "fcr_margin_discharge",
        "name": "FCR Available Margin Discharge",
        "field": FCR_MARGIN_DISCHARGE,
        "icon": "mdi:battery-minus",
        "native_unit": "kW",
    },
    {
        "key": "fcr_response_power",
        "name": "FCR Charge Discharge Power",
        "field": FCR_RESPONSE_POWER,
        "icon": "mdi:transmission-tower",
        "native_unit": "W",
    },
]

# ----------------------------------------------------------------------
# Metadata Sensors
# ----------------------------------------------------------------------

METADATA_SENSORS = [
    {
        "key": "fcr_bsp",
        "name": "FCR BSP",
        "icon": "mdi:transmission-tower",
    },
    {
        "key": "fcr_stream",
        "name": "FCR Stream",
        "icon": "mdi:transmission-tower",
    },
    {
        "key": "belpex_average",
        "name": "Belpex Average",
        "unit": "€/kWh",
        "icon": "mdi:currency-eur",
    },
    {
        "key": "aws_qos",
        "name": "AWS QoS",
        "unit": "%",
        "icon": "mdi:cloud-percent",
    },
    {
        "key": "bms_status",
        "name": "BMS Status",
        "icon": "mdi:battery-heart",
    },
    {
        "key": "bms_model",
        "name": "BMS Model",
        "icon": "mdi:battery",
    },
    {
        "key": "board_model",
        "name": "Board",
        "icon": "mdi:raspberry-pi",
    },
    {
        "key": "device_name",
        "name": "Device Name",
        "icon": "mdi:identifier",
    },
    {
        "key": "connected_status",
        "name": "Connected",
        "icon": "mdi:lan-connect",
    },
    {
        "key": "eastron_qos",
        "name": "Eastron QoS",
        "unit": "%",
        "icon": "mdi:percent",
    },
    {
        "key": "ev_status",
        "name": "EV",
        "icon" : "mdi:ev-station",
    },
    {
        "key": "ev_discovery",
        "name": "EV Discovery",
        "icon": "mdi:ev-station",
    },
    {
        "key": "inverter_status",
        "name": "Inverter Status",
        "icon" : "mdi:solar-power",
    },
    {
        "key": "inverter_meter",
        "name": "Inverter Meter",
        "icon" : "mdi:meter-electric",
    },
    {
        "key": "inverter_fw",
        "name": "Inverter FW",
        "icon" : "mdi:chip",
    },
    {
        "key": "inverter_serial",
        "name": "Inverter Serial",
        "icon" : "mdi:barcode",
    },
    {
        "key": "ioapi",
        "name": "IO API",
        "icon" : "mdi:api",
    },
    {
        "key": "iodaemon",
        "name": "IO Daemon",
        "icon" : "mdi:cog",
    },
    {
        "key": "iomanager",
        "name": "IO Manager",
        "icon" : "mdi:cog-transfer",
    },
    {
        "key": "update_status",
        "name": "Update Status",
        "icon" : "mdi:update",
    },
    {
        "key": "modbus_details",
        "name": "Modbus Details",
        "icon" : "mdi:serial-port",
    },
    {
        "key": "modbus_qos",
        "name": "Modbus QoS",
        "unit": "%",
        "icon" : "mdi:percent",
    },
    {
        "key": "modbus_adapter",
        "name": "Modbus Adapter",
        "icon" : "mdi:usb-port",
    },
    {
        "key": "p1_status",
        "name": "P1 Status",
        "icon" : "mdi:ethernet",
    },
    {
        "key": "p1_qos",
        "name": "P1 QoS",
        "unit": "%",
        "icon" : "mdi:percent",
    },
    {
        "key": "p1_gridtype",
        "name": "P1 Grid Type",
        "icon" : "mdi:transmission-tower",
    },
    {
        "key": "storage_details",
        "name": "Storage",
        "icon": "mdi:database",
    },
]

# ----------------------------------------------------------------------
# EMS Sensors
# ----------------------------------------------------------------------
EMSCONF_SENSORS = [
    {
        "key": "soc_lim_penalty",
        "name": "SOC Limit Penalty",
        "icon": "mdi:battery-alert",
    },
    {
        "key": "fcr_baseline_jump_penalty",
        "name": "FCR Baseline Jump Penalty",
        "icon": "mdi:chart-timeline-variant",
    },
    {
        "key": "fcr_shortfall_penalty",
        "name": "FCR Shortfall Penalty",
        "icon": "mdi:alert-octagon",
    },
    {
        "key": "implied_shortfall_additive_penalty",
        "name": "Implied Shortfall Additive Penalty",
        "icon": "mdi:plus-circle-outline",
    },
    {
        "key": "implied_shortfall_multiplicative_penalty",
        "name": "Implied Shortfall Multiplicative Penalty",
        "icon": "mdi:multiplication",
    },
    {
        "key": "fcr_allocation_jump_penalty",
        "name": "FCR Allocation Jump Penalty",
        "icon": "mdi:chart-sankey",
    },
    {
        "key": "lipschitz_constant",
        "name": "Lipschitz Constant",
        "icon": "mdi:function-variant",
    },
    {
        "key": "fcr_extra_soc_reserve",
        "name": "FCR Extra SOC Reserve",
        "unit": "%",
        "icon": "mdi:battery-plus",
    },
    {
        "key": "safe_max_fcr_allocation",
        "name": "Safe Max FCR Allocation",
        "unit": "%",
        "icon": "mdi:shield-check",
    },
    {
        "key": "expected_peak_activation_down",
        "name": "Expected Peak Activation Down",
        "icon": "mdi:chart-bell-curve",
    },
    {
        "key": "fcr_max_increase",
        "name": "FCR Max Increase",
        "icon": "mdi:arrow-up-bold",
    },
    {
        "key": "fcr_max_decrease",
        "name": "FCR Max Decrease",
        "icon": "mdi:arrow-down-bold",
    },
    {
        "key": "setpoint_transmisssion_error_penalty_factor",
        "name": "Setpoint Transmission Error Penalty Factor",
        "icon": "mdi:transmission-tower-off",
    },
    {
        "key": "enable_reserve_mode",
        "name": "Reserve Mode Enabled",
        "icon": "mdi:shield-lock",
    },
]
# ----------------------------------------------------------------------
# FCR TENDER Sensors
# ----------------------------------------------------------------------
FCR_TENDER_SENSORS = [
    {
        "key": "fcr_tender_price",
        "name": "FCR Tender Price",
        "icon": "mdi:chart-line",
    },
]

# ----------------------------------------------------------------------
# Websocket subscription
# ----------------------------------------------------------------------

WEBSOCKET_SUBSCRIPTIONS = [
    "listen/*",
]

# ----------------------------------------------------------------------
# Device names
# ----------------------------------------------------------------------

DEVICE_FLEXIO_STATUS = "FlexiO Status"
DEVICE_FCR = "FlexiO FCR"
DEVICE_METADATA = "FlexiO Metadata"