# LifePowr FlexiO

Home Assistant integration for the **LifePowr FlexiO Energy Management System**.

This integration connects directly to a local LifePowr FlexiO gateway using the built-in WebSocket interface and exposes diagnostics, telemetry, EMS configuration and FCR-related data to Home Assistant.

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.7%2B-blue)
![Version](https://img.shields.io/b
## Features

### Diagnostics

Exposes diagnostic information from the FlexiO gateway:

- AWS connectivity
- BMS status
- Inverter status
- P1 status
- Modbus status
- EV discovery
- IO Manager status
- Board information

### FCR Telemetry

Real-time FCR telemetry:

- FCR Baseline
- FCR Measurement
- FCR Error
- Available Charge Margin
- Available Discharge Margin
- Charge/Discharge Power

### FCR Tender Prices

Forecast-style entity exposing:

- Current FCR tender price
- Next price
- Maximum price
- Minimum price
- Average price
- Complete future forecast

### EMS Configuration

Access to EMS optimizer settings:

- SOC Limit Penalty
- FCR Baseline Jump Penalty
- FCR Shortfall Penalty
- Safe Max FCR Allocation
- FCR Reserve Settings
- Additional optimization parameters

### Metadata

Additional information:

- Device name
- Inverter serial number
- Firmware information
- Board model
- AWS QoS
- P1 QoS
- Modbus QoS

---

## Installation

### HACS

1. Open HACS
2. Integrations
3. Custom repositories
4. Add:

```
https://github.com/Wozzyke/lifepowr
```

5. Category:

```
Integration
```

6. Install
7. Restart Home Assistant

---

### Manual Installation

Copy:

```
custom_components/lifepowr
```

to:

```
config/custom_components/lifepowr
```

Restart Home Assistant.

---

## Configuration

1. Go to:

```
Settings
→ Devices & Services
→ Add Integration
```

2. Search for:

```
LifePowr FlexiO
```

3. Enter:

- Hostname
- IP address

Example:

```
192.168.1.100
```

---

## Requirements

- LifePowr FlexiO gateway
- Local network access
- Home Assistant 2026.7 or newer

---

## Known Limitations

This integration is based on local WebSocket communication with the FlexiO gateway.

Available entities depend on:

- FlexiO firmware version
- Enabled EMS functionality
- Available connected devices

---

## Support

### Issues

Please report bugs via GitHub:

https://github.com/Wozzyke/lifepowr/issues

### Feature Requests

Suggestions and contributions are welcome.

---

## Disclaimer

This project is not affiliated with or endorsed by LifePowr.

LifePowr and FlexiO are trademarks of their respective owners.

---

## License

MIT License