"""
py_now_playing - A Python library for interacting with the Now Playing API.
This library provides classes and functions to retrieve and manage information about the currently playing media,
including playback status, media timeline, and media details.
"""
from py_now_playing.dataclasses.media_timeline import MediaTimeline
from py_now_playing.dataclasses.playback_info import PlaybackInfo, MediaPlaybackStatus, MediaPlaybackType, MediaPlaybackAutoRepeatMode
from py_now_playing.core import PyNowPlaying
from py_now_playing.dataclasses.media_info import MediaInfo


__all__ = [
    "MediaTimeline",
    "PlaybackInfo",
    "MediaPlaybackStatus",
    "MediaPlaybackType",
    "MediaPlaybackAutoRepeatMode",
    "PyNowPlaying",
    "MediaInfo"
]
