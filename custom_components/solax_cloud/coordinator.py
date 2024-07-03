"""Coordinator for solaxcloud."""

from datetime import datetime, timedelta

from solaxcloud.solaxcloud import solaxcloud

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER


class solaxcloudCoordinator(DataUpdateCoordinator[dict[str, datetime]]):
    """Class to manage fetching solax cloud data."""

    def __init__(self, hass: HomeAssistant, api: solaxcloud) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, datetime]:
        """Fetch data from solax API."""

        dictionary = await self.hass.async_add_executor_job(self.api.get_realtime_data)

        return dictionary
