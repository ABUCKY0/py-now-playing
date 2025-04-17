"""Media Timeline Module
This module defines the MediaTimeline class, which encapsulates properties related to the media timeline,
including start time, end time, maximum seek time, current position, minimum seek time, and the last updated time.
It is used to manage and track the playback timeline of media content."""
from dataclasses import dataclass
from datetime import timedelta, datetime
@dataclass
class MediaTimeline:
  """Timeline properties of the media
  This class holds details about the media timeline such as start time, end time,"""
  
  start_time: timedelta
  end_time: timedelta
  max_seek_time: timedelta
  position: timedelta
  min_seek_time: timedelta
  last_updated_time: datetime
  
  def __init__(self):
    self.start_time = None
    self.end_time = None
    self.max_seek_time = None
    self.position = None
    self.min_seek_time = None
    self.last_updated_time = None
