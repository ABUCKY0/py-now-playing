"""This module defines the MediaInfo class, which holds information about the currently playing media."""
from dataclasses import dataclass
from PIL import Image
@dataclass
class MediaInfo:
  """Media Information Class
  This class holds details about the currently playing media, including artist, title, album information,
  track number, genres, playback type, and thumbnail image.

  Attributes:
    artist: Name of the artist
    title: Title of the media
    album_title: Title of the album
    album_artist: Artist of the album
    album_track_count: Number of tracks in the album
    track_number: Track number in the album
    genres: List of genres associated with the media
    playback_type: Type of playback (e.g., music, video)
    thumbnail: Thumbnail image of the media
  """
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
    """Initialize MediaInfo with default values."""
    self.artist = None
    self.title = None
    self.album_title = None
    self.album_artist = None
    self.album_track_count = None
    self.track_number = None
    self.genres = None
    self.playback_type = None
    self.thumbnail = None
    