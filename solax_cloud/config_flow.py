"""Config flow for Solax Cloud integration."""

from __future__ import annotations

from typing import Any

from requests.exceptions import ConnectTimeout, HTTPError
from solaxcloud.solaxcloud import solaxcloud
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import CONF_SERIAL, CONF_TOKEN, DOMAIN


class SolaxCloudConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solax Cloud."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Step when user initializes a integration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            token = user_input[CONF_TOKEN]
            serial = user_input[CONF_SERIAL]

            await self.async_set_unique_id(f"SolaxCloud_{serial}".strip())
            self._abort_if_unique_id_configured()

            api = solaxcloud(token=token, registration_number=serial)

            try:
                if not await self.hass.async_add_executor_job(
                    api.validate_token_and_registration_number
                ):
                    errors = {"base": "invalid_token_or_serial"}
            except (ConnectTimeout, HTTPError):
                errors = {"base": "cannot_connect"}

            if not errors:
                return self.async_create_entry(
                    title=f"{serial}".strip(), data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(
                    {
                        vol.Required(
                            CONF_TOKEN, default="XXXXXXXXXXXXXXXXXXXXXXX"
                        ): TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT)),
                        vol.Required(CONF_SERIAL, default="XXXXXXXXXX"): TextSelector(
                            TextSelectorConfig(type=TextSelectorType.TEXT)
                        ),
                    }
                ),
                user_input,
            ),
            errors=errors,
        )
