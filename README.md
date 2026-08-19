<p align="center">
  <img width="180px">docs/logo.png</img>
</p>

<h1 align="center">LifePowr FlexiO</h1>

<p align="center">
  Home Assistant integration for the LifePowr FlexiO Energy Management System
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Home%20Assistant-2026.7%2B-blue">
  <img src="https://img.shields.io/github/license/Wozzyke/lifepowr">
  <img src="https://img.shields.io/github/Wozzyke/lifepowr">
  <img src="https://img.shields.io/badge/HACS-Custom-orange">
</p>

---

The **LifePowr FlexiO** integration connects directly to a local FlexiO gateway using its WebSocket interface and exposes diagnostics, telemetry, EMS configuration and FCR-related data to Home Assistant.

---

# Features

## Diagnostics

Exposes diagnostic information from the FlexiO gateway:

- AWS connectivity
- BMS status
- Connected status
- EV discovery
- Inverter status
- IO Manager status
- Modbus status
- P1 status
- Board information

## FCR Telemetry

Real-time Frequency Containment Reserve (FCR) telemetry:

- FCR Baseline
- FCR Measurement
- FCR Error
- Available Charge Margin
- Available Discharge Margin
- Charge / Discharge Power

## FCR Tender Prices

Forecast-style entity exposing:

- Current tender price
- Next tender price
- Maximum forecast price
- Minimum forecast price
- Average forecast price
- Complete future price forecast

## EMS Configuration

Exposes EMS optimizer settings such as:

- SOC Limit Penalty
- FCR Baseline Jump Penalty
- FCR Shortfall Penalty
- FCR Allocation Penalty
- Safe Max FCR Allocation
- Reserve Mode Settings
- Additional optimization parameters

## Metadata

Additional FlexiO metadata:

- Device name
- Board model
- Inverter serial number
- Inverter firmware
- AWS QoS
- P1 QoS
- Modbus QoS
- Battery storage information
- Network information (IPv4, IPv6 and interface)

---

# Installation

## HACS

1. Open **HACS**
2. Navigate to **Integrations**
3. Open **Custom repositories**
4. Add:

```text
https://github.com/Wozzyke/lifepowr
```

5. Select:

```text
Integration
```

6. Install the integration
7. Restart Home Assistant

---

## Manual Installation

Copy:

```text
custom_components/lifepowr
```

to:

```text
config/custom_components/lifepowr
```

Restart Home Assistant.

---

# Configuration

1. Open:

```text
Settings
→ Devices & Services
```

2. Click:

```text
Add Integration
```

3. Search for:

```text
LifePowr FlexiO
```

4. Enter the hostname or IP address of the FlexiO gateway.

Example:

```text
192.168.1.100
```

---

# Requirements

- LifePowr FlexiO gateway
- Local network connectivity
- Home Assistant 2026.7 or newer

---

# Known Limitations

This integration is based on local WebSocket communication with the FlexiO gateway.

Available entities depend on:

- FlexiO firmware version
- Enabled EMS functionality
- Connected devices
- Available telemetry exposed by the gateway

---

# Known Issues

## Integration startup warning

Home Assistant may occasionally report that the LifePowr FlexiO integration is taking a long time to set up.

The current implementation starts WebSocket subscriptions immediately during initialization and begins processing incoming topic data straight away. This can trigger Home Assistant's startup watchdog, especially on slower systems.

The integration continues to function normally after startup.

This behavior is planned to be improved in a future release.

---

# Support

## Issues

Please report bugs via GitHub:
https://github.com/Wozzyke/lifepowr/issues

## Feature Requests

Suggestions and contributions are welcome.

---

# Disclaimer

This project is not affiliated with, endorsed by or supported by LifePowr.

LifePowr and FlexiO are trademarks of their respective owners.

---

# License

MIT License