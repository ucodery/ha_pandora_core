"""Adds config flow for wsdot."""

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, SOURCE_USER
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_USERNAME

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class PandoraConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Pandora."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        if user_input is None:
            return self.async_show_form(
                step_id=SOURCE_USER,
                data_schema=self.add_suggested_values_to_schema(vol.Schema({
                    vol.Optional(CONF_NAME, default=DOMAIN): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }), user_input),
                errors={},
            )

        await self.async_set_unique_id(user_input[CONF_USERNAME])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=user_input[CONF_NAME], data={})
