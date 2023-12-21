from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage.streams import DataReader
import json
import subprocess
from typing import List, Dict
from PIL import Image
import io
class NowPlaying:
    def __init__(self, media_manager: MediaManager = None):
        """Creates the NowPlaying Class

        @param MediaManager: The MediaManager to use
        """
        if media_manager is not None:
            self._manager = media_manager

    async def initalize_mediamanger(self) -> None:
        """Initalizes the MediaManager"""
        self._manager = await MediaManager.request_async()
    async def _get_sessions(self) -> List[MediaManager]:
        """Gets the sessions from the MediaManager
        
        @return: The sessions from the MediaManager
        """
        return self._manager.get_sessions()

    async def _get_app_user_model_ids(self) -> List[str]:
        """Gets the AppUserModelIds from the MediaManager

        @return: The AppUserModelIds from the MediaManager
        """
        sessions = await self._get_sessions()
        return [session.source_app_user_model_id for session in sessions]

    async def _get_now_playing_info(self, app_user_model_id: str) -> Dict[str, str] | None:
        """Gets the now playing info from the MediaManager
        
        @param app_user_model_id: The AppUserModelId to get the now playing info from
        @return: The now playing info from the MediaManager
        """
        sessions = await self._get_sessions()
        session = next(filter(lambda s: s.source_app_user_model_id == app_user_model_id, sessions), None)
        if session is not None:
            info = await session.try_get_media_properties_async()
            if info is not None:
                info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if not song_attr.startswith('_')}
                info_dict['genres'] = list(info_dict['genres'])
                return info_dict

        return None

    async def get_active_app_user_model_ids(self):
        """Gets the active AppUserModelIds
        
        @return: The active AppUserModelIds
        """
        amuids = subprocess.check_output(["powershell.exe", "Get-StartApps | ConvertTo-Json"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
        active_amuids = await self._get_app_user_model_ids()
        amuids = json.loads(amuids)
        return [app for app in amuids if app['AppID'] in active_amuids]

    async def get_now_playing(self, app_user_model_id: str = None):
        """Gets the now playing info from the MediaManager
        @param app_user_model_id: The AppUserModelId to get the now playing info from
        @return: The now playing info from the MediaManager
        """
        if app_user_model_id is not None:
            return await self._get_now_playing_info(app_user_model_id)
        else:
            app_ids = await self.get_active_app_audio_model_ids()
            for app_id in app_ids:
                info = await self._get_now_playing_info(app_id)
                if info is not None:
                    return info
        return None

    async def thumbnail_to_image(self, thumbnail):
        """Converts a thumbnail to a PIL Image
        
        @param thumbnail: The thumbnail to convert
        @return: The PIL Image
        """
        stream = await thumbnail.open_read_async()
        size = stream.size
        reader = stream.get_input_stream_at(0)
        data_reader = DataReader(reader)
        await data_reader.load_async(size)
        buffer = data_reader.read_buffer(size)
        byte_array = bytearray(buffer)
        image = Image.open(io.BytesIO(byte_array))
        return image