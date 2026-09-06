"""Solax cloud."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import solaxcloudCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add Solax cloud entry."""
    coordinator: solaxcloudCoordinator = hass.data[DOMAIN][entry.entry_id]

    assert entry.unique_id
    unique_id = entry.unique_id

    async_add_entities(
        SolaxCloudSensor(unique_id, description, coordinator)
        for description in SENSOR_TYPES
    )


class SolaxCloudSensor(CoordinatorEntity[solaxcloudCoordinator], SensorEntity):
    """Representation of a Solax cloud sensor."""

    def __init__(
        self,
        unique_id: str,
        description: SensorEntityDescription,
        coordinator: solaxcloudCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{unique_id}_test_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> datetime | None:
       """Return the state of the sensor."""
       if self.entity_description.key == "total_solar_power":
           # Calculate total solar production from all MPPT inputs
           data = self.coordinator.data
           total = 0.0
           for key in ["powerdc1", "powerdc2", "powerdc3", "powerdc4"]:
               value = data.get(key)
               if value is not None:
                   try:
                       total += float(value)
                   except (ValueError, TypeError):
                       pass
           return total
       if self.entity_description.key == "utcDateTime":
           # Parse ISO 8601 timestamp string to datetime object
           # Note: The API appears to return time in a timezone that's not actually UTC
           # Based on user report, it's 7 hours behind actual UTC
           value = self.coordinator.data.get(self.entity_description.key)
           if value is None:
               return None
           if isinstance(value, datetime):
               return value
           if isinstance(value, str):
               try:
                   # Handle ISO 8601 format: "2025-12-28T09:43:55Z"
                   # The API returns time that's 7 hours behind actual UTC
                   # Parse as naive datetime first, then add 7 hours to get correct UTC
                   iso_string = value.replace('Z', '')
                   dt = datetime.fromisoformat(iso_string)
                   # Add 7 hours to correct the timezone offset
                   dt_corrected = dt + timedelta(hours=7)
                   # Make it timezone-aware (UTC)
                   return dt_corrected.replace(tzinfo=timezone.utc)
               except (ValueError, TypeError, AttributeError):
                   return None
           return None
       return self.coordinator.data.get(self.entity_description.key)


SENSOR_TYPES = [
    SensorEntityDescription(
        key="inverterSn",
        name="Inverter serial",
        translation_key="inverter_serial",
    ),
    SensorEntityDescription(
        key="sn",
        name="Pocket serial",
        translation_key="pocket_serial",
    ),
    SensorEntityDescription(
        key="batPower",
        name="Battery power",
        translation_key="battery_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ratedPower",
        name="Inverter size",
        translation_key="inverter_size",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="idc1",
        name="MPPT1 current",
        translation_key="mppt1_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="idc2",
        name="MPPT2 current",
        translation_key="mppt2_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="vdc1",
        name="MPPT1 voltage",
        translation_key="mppt1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="vdc2",
        name="MPPT2 voltage",
        translation_key="mppt2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="iac1",
        name="AC phase 1 current",
        translation_key="ac_phase1_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="vac1",
        name="AC phase 1 voltage",
        translation_key="ac_phase1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="acpower",
        name="AC Power",
        translation_key="ac_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT
    ),
    SensorEntityDescription(
        key="temperature",
        name="Inverter Temperature",
        translation_key="inverter_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="yieldtoday",
        name="Yield today",
        translation_key="yield_today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="yieldtotal",
        name="Yield total",
        translation_key="yield_total",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="feedinpower",
        name="Feedin Power",
        translation_key="feedin_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerdc1",
        name="MPPT1 power",
        translation_key="mppt1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="powerdc2",
        name="MPPT2 power",
        translation_key="mppt2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="total_solar_power",
        name="Total Solar Power",
        translation_key="total_solar_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pac1",
        name="AC phase 1 power",
        translation_key="ac_phase1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pac2",
        name="AC phase 2 power",
        translation_key="ac_phase2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pac3",
        name="AC phase 3 power",
        translation_key="ac_phase3_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="iac2",
        name="AC phase 2 current",
        translation_key="ac_phase2_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="iac3",
        name="AC phase 3 current",
        translation_key="ac_phase3_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="vac2",
        name="AC phase 2 voltage",
        translation_key="ac_phase2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="vac3",
        name="AC phase 3 voltage",
        translation_key="ac_phase3_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="fac1",
        name="AC phase 1 frequency",
        translation_key="ac_phase1_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="fac2",
        name="AC phase 2 frequency",
        translation_key="ac_phase2_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="fac3",
        name="AC phase 3 frequency",
        translation_key="ac_phase3_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="feedinenergy",
        name="Feedin energy",
        translation_key="feedin_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="consumeenergy",
        name="Consume energy",
        translation_key="consume_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="uploadTime",
        name="Last cloud upload",
        translation_key="upload_time",
        # device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="utcDateTime",
        name="UTC Date Time",
        translation_key="utc_date_time",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="batVoltage",
        name="Battery voltage",
        translation_key="battery_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="batCurrent",
        name="Battery current",
        translation_key="battery current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="temperBoard",
        name="Battery temperature 1",
        translation_key="battery_temperature_1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="surplusEnergy",
        name="Surplus energy",
        translation_key="surplus_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="chargeEnergy",
        name="Charge energy",
        translation_key="charge_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="dischargeEnergy",
        name="Discharge energy",
        translation_key="discharge_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="acenergyin",
        name="Grid energy in",
        translation_key="grid_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="pvenergy",
        name="Feedin energy",
        translation_key="pv_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="soc",
        name="State of charge",
        translation_key="soc",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battemper",
        name="Battery temperature 2",
        translation_key="battery_temperature_2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="veps1",
        name="EPS phase 1 voltage",
        translation_key="eps_phase1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="veps2",
        name="EPS phase 2 voltage",
        translation_key="eps_phase2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="veps3",
        name="EPS phase 3 voltage",
        translation_key="eps_phase3_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ieps1",
        name="EPS phase 1 current",
        translation_key="eps_phase1_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ieps2",
        name="EPS phase 2 current",
        translation_key="eps_phase2_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ieps3",
        name="EPS phase 3 current",
        translation_key="eps_phase3_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="peps1",
        name="EPS phase 1 power",
        translation_key="eps_phase1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="peps2",
        name="EPS phase 2 power",
        translation_key="eps_phase2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="peps3",
        name="EPS phase 3 power",
        translation_key="eps_phase3_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="epsfreq",
        name="EPS frequency",
        translation_key="eps_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="batcycle",
        name="Battery cycle count",
        translation_key="batcycle",
    ),
]
