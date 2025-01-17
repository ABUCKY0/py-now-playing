from dataclasses import dataclass
from PIL import Image
from winrt.windows.media import MediaPlaybackType
@dataclass
class MediaInfo:
  artist: str
  title: str
  album_title: str
  album_artist: str
  album_track_count: int
  track_number: int
  genres: list
  playback_type: str
  thumbnail: Image
  
  def __init__(self):
    self.artist = None
    self.title = None
    self.album_title = None
    self.album_artist = None
    self.album_track_count = None
    self.track_number = None
    self.genres = None
    self.playback_type = None
    self.thumbnail = None