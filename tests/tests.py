import unittest
# import asynctest
from unittest.mock import MagicMock, patch
from py_now_playing import MediaPlaybackStatus, MediaPlaybackType, MediaPlaybackAutoRepeatMode, PlaybackInfo, MediaTimeline, PlaybackControls, MediaInfo
import logging
import time 
import flet as ft
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
  
  pbc = PlaybackControls(
      await PlaybackControls.get_aumid_by_name("Media Player"))
  logger.info("Initalizing MediaManager")
  await pbc.initalize_mediamanager()  
  # logger.info("Pausing media")
  # await pbc.pause()
  # time.sleep(1)
  
  # logger.info("Playing media")
  # logger.info("was successful?" + str(await pbc.play()))
  
  # logger.info("Toggling play/pause")
  # await pbc.toggle_play_pause()
  # time.sleep(1)
  # await pbc.toggle_play_pause()
  # #logger.info("Stopping media")
  # #await pbc.stop()
  # await pbc.record()
  # await pbc.rewind()
  # time.sleep(1)
  # await pbc.previous_track()
  # time.sleep(1)
  # await pbc.next_track()
  #logger.info(await pbc.get_timeline_properties())
  await pbc.change_playback_rate(1.0)
  
  # # open thumbnail in photo viewer
  # thumbnail = await pbc.get_thumbnail()
  # thumbnail.show()
  
  await pbc.change_shuffle_active(True)
  
  def timeline_properties_changed(sender, args: MediaTimeline):
    logger.info("Timeline properties changed")
    logger.info(args)
  
  pbc.register_timeline_properties_changed_callback(timeline_properties_changed)
  
  
  def playback_info_changed(sender, args: PlaybackInfo):
    logger.info("Playback info changed")
    logger.info(args)
  
  pbc.register_playback_info_changed_callback(playback_info_changed)
  
  def media_properties_changed(sender, args: MediaInfo):
    logger.info("Media properties changed")
    logger.info(args)
    
  pbc.register_media_properties_changed_callback(media_properties_changed)
  time.sleep(5)
  # stop
  await pbc.stop()
  
  while(True):
    time.sleep(1)
  
  
asyncio.run(main_test())

