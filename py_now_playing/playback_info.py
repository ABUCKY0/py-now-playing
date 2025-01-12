from dataclasses import dataclass
import enum


class MediaPlaybackStatus(enum.IntEnum):
  """Playback status of the media
  Taken from winrt.Windows.Media.Playback.MediaPlaybackStatus
  """
  CLOSED = 0
  CHANGING = 2
  STOPPED = 3
  PLAYING = 4
  PAUSED = 5

class MediaPlaybackType(enum.IntEnum):
  UNKNOWN = 0
  MUSIC = 1
  VIDEO = 2
  IMAGE = 3

class MediaPlaybackAutoRepeatMode(enum.IntEnum):
  NONE = 0
  TRACK = 1
  LIST = 2
  

@dataclass
class PlaybackInfo:
  playback_type: MediaPlaybackType
  playback_status: MediaPlaybackStatus
  playback_rate: float
  auto_repeat_mode: MediaPlaybackAutoRepeatMode
  is_shuffle_active: bool
  
  def __init__(self) -> None:
    self.playback_type = None
    self.playback_status = None
    self.playback_rate = None
    self.auto_repeat_mode = None
    self.is_shuffle_active = None
  