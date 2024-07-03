"""Solax cloud."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import solaxcloudCoordinator

ISSUE_PLACEHOLDER = {"url": "/config/integrations/dashboard/add?domain=solaxcloud"}


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
       #print("called")
       """Return the state of the sensor."""
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
        key="ratedPower",
        name="Inverter size",
        translation_key="inverter_size",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
    ),
    SensorEntityDescription(
        key="idc1",
        name="MPPT1 current",
        translation_key="mppt1_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="idc2",
        name="MPPT2 current",
        translation_key="mppt2_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="vdc1",
        name="MPPT1 voltage",
        translation_key="mppt1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="vdc2",
        name="MPPT2 voltage",
        translation_key="mppt2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="iac1",
        name="AC phase 1 current",
        translation_key="ac_phase1_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="vac1",
        name="AC phase 1 voltage",
        translation_key="ac_phase1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="acpower",
        name="AC Power",
        translation_key="ac_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="temperature",
        name="Inverter Temperature",
        translation_key="inverter_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="yieldtoday",
        name="Yield today",
        translation_key="yield_today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
    ),
    SensorEntityDescription(
        key="yieldtotal",
        name="Yield total",
        translation_key="yield_total",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
    ),
    SensorEntityDescription(
        key="feedinpower",
        name="Feedin Power",
        translation_key="feedin_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="powerdc1",
        name="MPPT1 power",
        translation_key="mppt1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="powerdc2",
        name="MPPT2 power",
        translation_key="mppt2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="pac1",
        name="AC phase 1 power",
        translation_key="ac_phase1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="pac2",
        name="AC phase 2 power",
        translation_key="ac_phase2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="pac3",
        name="AC phase 3 power",
        translation_key="ac_phase3_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="iac2",
        name="AC phase 2 current",
        translation_key="ac_phase2_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="iac3",
        name="AC phase 3 current",
        translation_key="ac_phase3_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="vac2",
        name="AC phase 2 voltage",
        translation_key="ac_phase2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="vac3",
        name="AC phase 3 voltage",
        translation_key="ac_phase3_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="fac1",
        name="AC phase 1 frequency",
        translation_key="ac_phase1_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
    ),
    SensorEntityDescription(
        key="fac2",
        name="AC phase 2 frequency",
        translation_key="ac_phase2_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
    ),
    SensorEntityDescription(
        key="fac3",
        name="AC phase 3 frequency",
        translation_key="ac_phase3_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
    ),
    SensorEntityDescription(
        key="feedinenergy",
        name="Feedin energy",
        translation_key="feedin_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="consumeenergy",
        name="Consume energy",
        translation_key="consume_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="uploadTime",
        name="Last cloud upload",
        translation_key="upload_time",
        # device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="batVoltage",
        name="Battery voltage",
        translation_key="battery_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="batCurrent",
        name="Battery current",
        translation_key="battery current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="temperBoard",
        name="Battery temperature 1",
        translation_key="battery_temperature_1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="surplusEnergy",
        name="Surplus energy",
        translation_key="surplus_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="chargeEnergy",
        name="Charge energy",
        translation_key="charge_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="dischargeEnergy",
        name="Discharge energy",
        translation_key="discharge_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="acenergyin",
        name="Grid energy in",
        translation_key="grid_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="pvenergy",
        name="Feedin energy",
        translation_key="pv_energy",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="soc",
        name="State of charge",
        translation_key="soc",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="battemper",
        name="Battery temperature 2",
        translation_key="battery_temperature_2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="veps1",
        name="EPS phase 1 voltage",
        translation_key="eps_phase1_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="veps2",
        name="EPS phase 2 voltage",
        translation_key="eps_phase2_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="veps3",
        name="EPS phase 3 voltage",
        translation_key="eps_phase3_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="ieps1",
        name="EPS phase 1 current",
        translation_key="eps_phase1_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="ieps2",
        name="EPS phase 2 current",
        translation_key="eps_phase2_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="ieps3",
        name="EPS phase 3 current",
        translation_key="eps_phase3_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="peps1",
        name="EPS phase 1 power",
        translation_key="eps_phase1_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="peps2",
        name="EPS phase 2 power",
        translation_key="eps_phase2_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="peps3",
        name="EPS phase 3 power",
        translation_key="eps_phase3_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    SensorEntityDescription(
        key="epsfreq",
        name="EPS frequency",
        translation_key="eps_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement="Hz",
    ),
    SensorEntityDescription(
        key="batcycle",
        name="Battery cycle count",
        translation_key="batcycle",
    ),
]
