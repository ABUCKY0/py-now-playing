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
  artist: str | None = None
  title: str | None = None
  album_title: str | None = None
  album_artist: str | None = None
  album_track_count: int | None = None
  track_number: int | None = None
  genres: list | None = None
  playback_type: str | None = None
  thumbnail: Image.Image | None = None
