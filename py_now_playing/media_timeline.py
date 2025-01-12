from dataclasses import dataclass
from datetime import timedelta, datetime
@dataclass
class MediaTimeline:
  """Timeline properties of the media"""
  
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