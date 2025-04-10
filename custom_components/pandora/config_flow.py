"""Adds config flow for wsdot."""

import logging
from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class PandoraConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Pandora."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_setup_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""

        return self.async_create_entry(title=f"{DOMAIN}_entry", data={})
