"""The Solax Cloud integration."""

from __future__ import annotations

from requests.exceptions import ConnectTimeout, HTTPError
from solaxcloud.solaxcloud import solaxcloud

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from homeassistant.helpers.issue_registry import IssueSeverity, async_create_issue

from .const import CONF_SERIAL, CONF_TOKEN, DOMAIN
from .coordinator import solaxcloudCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Solax Cloud from a config entry."""

    api = solaxcloud(
        token=entry.data[CONF_TOKEN],
        registration_number=entry.data[CONF_SERIAL],
    )

    try:
        valid = await hass.async_add_executor_job(
            api.validate_token_and_registration_number
        )
    except (ConnectTimeout, HTTPError) as ex:
        raise ConfigEntryNotReady from ex

    if not valid:
        async_create_issue(
            hass,
            DOMAIN,
            "Not a valid token or serialnumber(1)",
            is_fixable=False,
            issue_domain=DOMAIN,
            severity=IssueSeverity.ERROR,
            translation_key="not_valid",
            translation_placeholders={
                CONF_TOKEN: entry.data[CONF_TOKEN],
                CONF_SERIAL: entry.data[CONF_SERIAL],
            },
        )
        raise ConfigEntryError("Not a valid token or serialnumber(2)")

    coordinator = solaxcloudCoordinator(hass, api)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Solax config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
