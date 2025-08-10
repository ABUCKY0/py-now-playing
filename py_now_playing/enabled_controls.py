from dataclasses import dataclass

@dataclass
class EnabledControls:
    channel_down: bool | None = None
    channel_up: bool | None = None
    fast_forward: bool | None = None
    next_track: bool | None = None
    pause: bool | None = None
    playback_position: bool | None = None
    playback_rate: bool | None = None
    play : bool | None = None
    toggle_play_pause: bool | None = None
    previous_track: bool | None = None
    record: bool | None = None
    repeat: bool | None = None
    rewind: bool | None = None
    shuffle: bool | None = None
    stop: bool | None = None