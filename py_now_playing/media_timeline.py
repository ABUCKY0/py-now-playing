"""Media Timeline Module
This module defines the MediaTimeline class, which encapsulates properties related to the media timeline,
including start time, end time, maximum seek time, current position, minimum seek time, and the last updated time.
It is used to manage and track the playback timeline of media content."""
from dataclasses import dataclass
from datetime import timedelta, datetime
@dataclass
class MediaTimeline:
  """Timeline properties of the media
  This class holds details about the media timeline such as start time, end time, maximum seek time, current position, minimum seek time, and the last updated time.
  """

  start_time: timedelta | None = None
  end_time: timedelta | None = None
  max_seek_time: timedelta | None = None
  position: timedelta | None = None
  min_seek_time: timedelta | None = None
  last_updated_time: datetime | None = None
