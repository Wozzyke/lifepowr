"""Config flow for LifePowr FlexiO."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import callback

from .const import DOMAIN


class LifepowrConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for LifePowr."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):
        """Handle the initial step."""

        errors = {}

        if user_input is not None:

            host = user_input[CONF_HOST]

            #
            # Prevent duplicate entries
            #
            await self.async_set_unique_id(
                host
            )

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"LifePowr ({host})",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_HOST
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry,
    ):
        """Return options flow."""

        return LifepowrOptionsFlow(
            config_entry
        )


class LifepowrOptionsFlow(
    config_entries.OptionsFlow
):
    """Options flow."""

    def __init__(
        self,
        config_entry,
    ) -> None:

        self.config_entry = (
            config_entry
        )

    async def async_step_init(
        self,
        user_input=None,
    ):
        """Manage options."""

        if user_input is not None:

            return (
                self.async_create_entry(
                    title="",
                    data=user_input,
                )
            )

        return (
            self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(
                    {}
                ),
            )
        )