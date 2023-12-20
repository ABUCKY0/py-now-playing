import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
import json
import subprocess
from typing import List, Optional, Dict

class NowPlaying:
    def __init__(self):
        self._manager = None

    @classmethod
    async def create(cls) -> 'NowPlaying':
        self = NowPlaying()
        self._manager = await MediaManager.request_async()
        return self

    async def _get_sessions(self):
        return self._manager.get_sessions()

    async def _get_app_user_model_ids(self) -> List[str]:
        sessions = await self._get_sessions()
        return [session.source_app_user_model_id for session in sessions]

    async def _get_now_playing_info(self, app_user_model_id: str) -> Optional[Dict[str, str]]:
        sessions = await self._get_sessions()
        for session in sessions:
            if session.source_app_user_model_id == app_user_model_id:
                try:
                    info = await session.try_get_media_properties_async()
                    if info is not None:
                        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if not song_attr.startswith('_')}
                        info_dict['genres'] = list(info_dict['genres'])
                        return info_dict
                except Exception as e:
                    print(f"Failed to get media properties: {e}")
        return None

    async def get_active_app_audio_model_ids(self):
        amuids = subprocess.check_output(["powershell.exe", "Get-StartApps | ConvertTo-Json"], shell=False)
        active_amuids = await self._get_app_user_model_ids()
        amuids = json.loads(amuids)
        return [app for app in amuids if app['AppID'] in active_amuids]

    async def get_now_playing(self, app_user_model_id: str = None):
        if app_user_model_id is not None:
            return await self._get_now_playing_info(app_user_model_id)
        else:
            app_ids = await self.get_active_app_audio_model_ids()
            for app_id in app_ids:
                info = await self._get_now_playing_info(app_id)
                if info is not None:
                    return info
        return None