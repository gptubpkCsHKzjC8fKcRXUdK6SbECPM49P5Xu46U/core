"""Support for Plaato Airlock sensors."""
from __future__ import annotations

from pyplaato.plaato import PlaatoKeg

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .const import CONF_USE_WEBHOOK, COORDINATOR, DOMAIN
from .entity import PlaatoEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Plaato from a config entry."""

    if config_entry.data[CONF_USE_WEBHOOK]:
        return

    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    async_add_entities(
        PlaatoBinarySensor(
            hass.data[DOMAIN][config_entry.entry_id],
            sensor_type,
            coordinator,
        )
        for sensor_type in coordinator.data.binary_sensors
    )


class PlaatoBinarySensor(PlaatoEntity, BinarySensorEntity):
    """Representation of a Binary Sensor."""

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self._coordinator is not None:
            return self._coordinator.data.binary_sensors.get(self._sensor_type)
        return False

    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        """Return the class of this device, from BinarySensorDeviceClass."""
        if self._coordinator is None:
            return None
        if self._sensor_type is PlaatoKeg.Pins.LEAK_DETECTION:
            return BinarySensorDeviceClass.PROBLEM
        if self._sensor_type is PlaatoKeg.Pins.POURING:
            return BinarySensorDeviceClass.OPENING
