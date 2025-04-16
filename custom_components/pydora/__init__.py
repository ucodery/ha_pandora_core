"""The pandora component."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant

import pandora.clientbuilder
import pydora.configure


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pydora from a config entry."""

    pandora_api_config = (await hass.async_add_executor_job(pydora.configure.PandoraKeysConfigParser().load))["android"]
    
    client = pandora.clientbuilder.SettingsDictBuilder({
        "DECRYPTION_KEY": pandora_api_config["decryption_key"], 
        "ENCRYPTION_KEY": pandora_api_config["encryption_key"], 
        "PARTNER_USER": pandora_api_config["username"],
        "PARTNER_PASSWORD": pandora_api_config["password"],
        "DEVICE": pandora_api_config["device"], 
        "API_HOST": pandora_api_config["api_host"],
    }).build()

    await hass.async_add_executor_job(client.login, entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])

    entry.client = client
    return True
