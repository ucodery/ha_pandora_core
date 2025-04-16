from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source import MediaSource, MediaSourceItem, BrowseMediaSource, PlayMedia
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_get_media_source(hass: HomeAssistant) -> MediaSource:
    """Set up Pandora media source."""

    return PandoraMediaSource(hass)


class PandoraMediaSource(MediaSource):
    """Provide Pandora Radio as a media source."""

    name = "Pydora"

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(DOMAIN)
        self.hass = hass
        self.client = hass.config_entries.async_entries(DOMAIN)[0].client

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        station = await self.hass.async_add_executor_job(self.client.get_station, item.identifier)
        playlist = await self.hass.async_add_executor_job(station.get_playlist)
        song = next(playlist)

        mime = "audio/aac" if song.encoding == "aacplus" else song.encoding
        return PlayMedia(song.audio_url, mime)

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.CHANNEL,
            media_content_type=MediaType.MUSIC,
            title="Pandora Stations",
            can_play=False,
            can_expand=False,
            children=[
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=station.id,
                    media_class=MediaClass.MUSIC,
                    media_content_type=MediaType.MUSIC,
                    title=station.name,
                    thumbnail=station.art_url,
                    can_play=True,
                    can_expand=False,
                )
                for station in await self.hass.async_add_executor_job(self.client.get_station_list)
            ],
        )
