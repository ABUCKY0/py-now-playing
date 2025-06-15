import unittest
# import asynctest
from unittest.mock import MagicMock, patch
from py_now_playing import MediaPlaybackStatus, MediaPlaybackType, MediaPlaybackAutoRepeatMode, PlaybackInfo, MediaTimeline, PyNowPlaying, MediaInfo
import logging
import time 
# import flet as ft
from winrt.windows.media.control import TimelinePropertiesChangedEventArgs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import asyncio

async def main_test():
  # logger.info("Creating NowPlaying object")
  # np = NowPlaying()
  
  # logger.info("Initalizing MediaManager")
  # await np.initalize_mediamanager()
  
  # logger.info("Getting active app user model ids")
  # print(await NowPlaying.get_active_app_user_model_ids())
  
  # logger.info("Getting media info")
  # print(await np.get_now_playing('ChromeDev._crx_hjlgoickghknhfichlenalencg'))
  
  
  logger.info("Creating PlaybackControls object")
  amuids = await PyNowPlaying.get_active_app_user_model_ids()
  print(list(filter(lambda name: name['Name'] == "Amazon Music", amuids))[0])
  pbc = PyNowPlaying(
      list(filter(lambda name: name['Name'] == "Amazon Music", amuids))[0]['AppID']
  )
  logger.info("Initalizing MediaManager")
  await pbc.initalize_mediamanager()
  while True:
    try:
      print(f"WinRT {(await pbc.get_timeline_properties()).position}")
      print(f"Live  {(await pbc.get_interpolated_timeline_properties()).position}")
    except Exception:
      pass
    time.sleep(2)


asyncio.run(main_test())

