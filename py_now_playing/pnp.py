"""Py Now Playing - Playback Controls Module
This module provides the PlaybackControls class, which allows interaction with media playback controls on Windows.
It includes methods to control playback, retrieve media information, and register callbacks for media events."""
import asyncio
import io
from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    PlaybackInfoChangedEventArgs,
    TimelinePropertiesChangedEventArgs,
    MediaPropertiesChangedEventArgs,


)
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSession

from winrt.windows.storage.streams import DataReader
import logging
from subprocess import check_output, CREATE_NO_WINDOW
from json import loads
from .media_info import MediaInfo
from .media_timeline import MediaTimeline
from .playback_info import PlaybackInfo
from PIL import Image
logger = logging.getLogger(__name__)


class PlaybackControls:
  """Playback Controls Class
  This class provides methods to control media playback and retrieve media information.
  It interacts with the Windows Media Control API to manage playback sessions.
  
  Attributes:
      aumid (str): The AppUserModelId of the application.
      media_manager (MediaManager, optional): The MediaManager instance for managing media sessions.
      """
  def __init__(self, aumid: str, media_manager: MediaManager = None):
    """Initializes the PlaybackControls.

    Args:
        aumid (str): The AppUserModelId of the application.
        media_manager (MediaManager, optional): The MediaManager instance. Defaults to None.

    Raises:
        ValueError: If aumid is None.
    """
    self.aumid = aumid

    if aumid is None:
      raise ValueError("aumid cannot be None")
    if media_manager is not None:
      self._manager = media_manager
    if media_manager is None:
      logger.debug(
          "Please run initalize_mediamanager for py_now_playing to properly function"
      )
      
    self._user_timeline_properties_callback = None
    self._user_playback_info_callback = None
    self._user_media_properties_callback = None

  async def initalize_mediamanager(self) -> None:
    """Initalizes the MediaManager"""
    self._manager = await MediaManager.request_async()

  async def get_timeline_properties(self) -> MediaTimeline:
    """Gets the timeline properties of the media.

    Returns:
        MediaTimeline: The timeline properties of the media.
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      timeline_properties = session.get_timeline_properties()
      tp = MediaTimeline()
      tp.start_time = timeline_properties.start_time
      tp.end_time = timeline_properties.end_time
      tp.max_seek_time = timeline_properties.max_seek_time
      tp.position = timeline_properties.position
      tp.min_seek_time = timeline_properties.min_seek_time
      tp.last_updated_time = timeline_properties.last_updated_time
      return tp

  async def get_thumbnail(self) -> Image:
    """Gets the thumbnail of the media.

    Returns:
        Image: The thumbnail of the media as a PIL Image.
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      thumbnail = (await session.try_get_media_properties_async()).thumbnail
      return await self.thumbnail_to_image(thumbnail)

  async def get_media_info(self) -> MediaInfo | None:
    """Gets the media info of the media.

    Returns:
        MediaInfo: The media info of the media.
    """
    sessions = self._manager.get_sessions()
    session = next(filter(lambda s: s.source_app_user_model_id ==
                    self.aumid, sessions), None)
    info_dict = None
    if session is not None:
      info = await session.try_get_media_properties_async()
      if info is not None:
        info_dict = {song_attr: getattr(info, song_attr) for song_attr in dir(info) if not song_attr.startswith('_')}
        info_dict['genres'] = list(info_dict['genres'])

    if self.aumid is not None:
      info = info_dict
      if info is None:
        return None
      song_info_object = MediaInfo()
      song_info_object.artist = info['artist']
      song_info_object.title = info['title']
      song_info_object.album_title = info['album_title']
      song_info_object.album_artist = info['album_artist']
      song_info_object.album_track_count = info['album_track_count']
      song_info_object.track_number = info['track_number']
      song_info_object.genres = info['genres']
      song_info_object.playback_type = info['playback_type']
      song_info_object.thumbnail = await self.thumbnail_to_image(info['thumbnail'])
      return song_info_object

  async def get_playback_info(self) -> PlaybackInfo | None:
    """Gets the playback info of the media.

    Returns:
        PlaybackInfo: The playback info of the media.
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      playback_info = session.get_playback_info()
      if playback_info is None:
        return None
      pi = PlaybackInfo()
      pi.playback_type = playback_info.playback_type
      pi.playback_status = playback_info.playback_status
      pi.playback_rate = playback_info.playback_rate
      pi.auto_repeat_mode = playback_info.auto_repeat_mode
      pi.is_shuffle_active = playback_info.is_shuffle_active
      return pi
    return None

  async def pause(self) -> bool:
    """Pause the media

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_pause_async()
    return False

  async def play(self) -> bool:
    """Play the media

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_play_async()
    return False

  async def toggle_play_pause(self) -> bool:
    """Toggle play/pause the media

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_toggle_play_pause_async()
    return False

  async def stop(self) -> bool:
    """Stop the media

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_stop_async()
    return False

  async def record(self) -> bool:
    """Tell the application to record

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_record_async()
    return False

  async def rewind(self) -> bool:
    """Rewind the media

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_rewind_async()
    return False

  async def fast_forward(self) -> bool:
    """Fast forward the media

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_fast_forward_async()
    return False

  async def next_track(self) -> bool:
    """Skip to the next track

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_skip_next_async()
    return False

  async def previous_track(self) -> bool:
    """Skip to the previous track

    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_skip_previous_async()
    return False

  async def thumbnail_to_image(self, thumbnail) -> Image.Image | None:
    """Converts a thumbnail to a PIL Image.

    Args:
        thumbnail: The thumbnail to convert.

    Returns:
        Image: The PIL Image.
    """

    if thumbnail is None:
      return None
    stream = await thumbnail.open_read_async()
    size = stream.size
    reader = stream.get_input_stream_at(0)
    data_reader = DataReader(reader)
    await data_reader.load_async(size)
    buffer = data_reader.read_buffer(size)
    byte_array = bytearray(buffer)
    image = Image.open(io.BytesIO(byte_array))
    return image

  @staticmethod
  async def get_active_app_user_model_ids() -> list:
    """Gets AppUserModelIds of apps which are actively playing media.

    Returns:
        list: The active AppUserModelIds.
    """
    amuids = check_output(["powershell.exe", "Get-StartApps | ConvertTo-Json"],
                          shell=False, creationflags=CREATE_NO_WINDOW)
    mediamanager = await MediaManager.request_async()
    sessions = mediamanager.get_sessions()
    active_amuids = [session.source_app_user_model_id for session in sessions]
    amuids = loads(amuids)
    return [app for app in amuids if app['AppID'] in active_amuids]

  @staticmethod
  async def get_aumid_by_name(name: str) -> str | None:
    """Gets the AUMID by the name of the app.

    Args:
        name (str): The name of the app.

    Returns:
        str: The AUMID of the app.
    """
    amuids = check_output(["powershell.exe", "Get-StartApps | ConvertTo-Json"],
                          shell=False, creationflags=CREATE_NO_WINDOW)
    amuids = loads(amuids)
    for app in amuids:
      if app['Name'] == name:
        return app['AppID']
    return None

  @staticmethod
  async def search_aumid_by_name(name: str) -> str | None:
    """Searches for the AUMID by the name of the app.

    Args:
        name (str): The name of the app to search for.

    Returns:
        str: The AUMID of the app.
    """
    amuids = check_output(["powershell.exe", "Get-StartApps | ConvertTo-Json"],
                          shell=False, creationflags=CREATE_NO_WINDOW)
    amuids = loads(amuids)
    matches = []
    for app in amuids:
      if name.lower() in app['Name'].lower():
        matches.append(app)
    return None

  async def change_playback_rate(self, rate: float) -> bool:
    """Changes the playback rate for supported apps/media.

    Args:
        rate (float): The new playback rate.
    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_change_playback_rate_async(rate)
    return False

  async def change_shuffle_active(self, state: bool) -> bool:
    """Changes the shuffle active state.

    Args:
        state (bool): The new shuffle active state.
    Returns:
        bool: True if successful, False
    """
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      return await session.try_change_shuffle_active_async(state)
    return False

  def _internal_playback_info_changed_callback(self, sender: GlobalSystemMediaTransportControlsSession, args: PlaybackInfoChangedEventArgs) -> None:
    """Internal callback for playback info changes.

    Args:
        sender (GlobalSystemMediaTransportControlsSession): The media session.
        args (PlaybackInfoChangedEventArgs): The event arguments.
    """
    reformatted_data = PlaybackInfo()
    reformatted_data.playback_type = sender.get_playback_info().playback_type
    reformatted_data.playback_status = sender.get_playback_info().playback_status
    reformatted_data.playback_rate = sender.get_playback_info().playback_rate
    reformatted_data.auto_repeat_mode = sender.get_playback_info().auto_repeat_mode
    reformatted_data.is_shuffle_active = sender.get_playback_info().is_shuffle_active
    self._user_playback_info_callback(sender, reformatted_data)
    return

  def _internal_timeline_properties_changed_callback(self, sender: GlobalSystemMediaTransportControlsSession, args: TimelinePropertiesChangedEventArgs) -> None:
    """Internal callback for timeline properties changes.

    Args:
        sender (GlobalSystemMediaTransportControlsSession): The media session.
        args (TimelinePropertiesChangedEventArgs): The event arguments.
    """
    reformatted_data = MediaTimeline()
    reformatted_data.start_time = sender.get_timeline_properties().start_time
    reformatted_data.end_time = sender.get_timeline_properties().end_time
    reformatted_data.max_seek_time = sender.get_timeline_properties().max_seek_time
    reformatted_data.position = sender.get_timeline_properties().position
    reformatted_data.min_seek_time = sender.get_timeline_properties().min_seek_time
    reformatted_data.last_updated_time = sender.get_timeline_properties().last_updated_time
    if self._user_timeline_properties_callback:
      self._user_timeline_properties_callback(sender, reformatted_data)

  def _internal_media_properties_changed_callback(self, sender: GlobalSystemMediaTransportControlsSession, args: MediaPropertiesChangedEventArgs) -> None:
    """Internal callback for media properties changes.

    Args:
        sender (GlobalSystemMediaTransportControlsSession): The media session.
        args (MediaPropertiesChangedEventArgs): The event arguments.
    """
    reformatted_data = MediaInfo()

    async def get_media_properties() -> MediaInfo:
      return await sender.try_get_media_properties_async()

    info = asyncio.run(get_media_properties())

    reformatted_data.artist = info.artist
    reformatted_data.title = info.title
    reformatted_data.album_title = info.album_title
    reformatted_data.album_artist = info.album_artist
    reformatted_data.album_track_count = info.album_track_count
    reformatted_data.track_number = info.track_number
    reformatted_data.genres = list(info.genres)
    reformatted_data.playback_type = info.playback_type

    async def get_thumbnail():
      return await self.thumbnail_to_image(info.thumbnail)

    reformatted_data.thumbnail = asyncio.run(get_thumbnail())

    if self._user_media_properties_callback:
      self._user_media_properties_callback(sender, reformatted_data)

  def register_playback_info_changed_callback(self, callback) -> None:
    """Registers a callback for playback info changes.

    Args:
        callback: The callback function.
    """
    self._user_playback_info_callback = callback
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      session.add_playback_info_changed(
          self._internal_playback_info_changed_callback)

  def register_timeline_properties_changed_callback(self, callback) -> None:
    """Registers a callback for timeline properties changes.

    Args:
        callback: The callback function.
    """
    self._user_timeline_properties_callback = callback
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      session.add_timeline_properties_changed(
          self._internal_timeline_properties_changed_callback)

  def register_media_properties_changed_callback(self, callback) -> None:
    """Registers a callback for media properties changes.

    Args:
        callback: The callback function.
    """
    self._user_media_properties_callback = callback
    sessions = self._manager.get_sessions()
    session = next(
        filter(lambda s: s.source_app_user_model_id == self.aumid, sessions), None)
    if session is not None:
      session.add_media_properties_changed(
          self._internal_media_properties_changed_callback)
