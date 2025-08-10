# Py Now Playing

This project started as me wanting to create a Discord RPC that would take the currently playing audio from a specified application, and put that onto my Discord activity. I found some windows apis that allow me to do this, however they weren't intuitive to use. So, I started this. 

Note that this class utilizes asyncio, so you may need to use await when using this class.

# Importing
You can use the following import statement to import all parts of py_now_playing
```py
from py_now_playing import *
```

# Setup
Initalizing a PyNowPlaying instance requires knowing the AppUserModelID of the app you want to get the media from. The PyNowPlaying class provides two static methods to help with this.

```py
async def get_active_app_user_model_ids() -> list:
```
Returns all apps currently playing media and their AppIDs as a list of dictionaries with the format {Name, AppID}

```py
async def get_all_aumids_by_name(name: str) -> list | None
```
Returns all apps on the system that contain the provided name case insensitive.

> Alternatively, if you wish to access a specific app all the time (as is the case with my Discord RPC Example), you can use the code above to find the AppID and then hardcode it, or run `Get-StartApps | Select-String "App Name"` in a Powershell window.

# Initalization

```python
pnp = await PyNowPlaying.create("Spotify.exe")
```

# Usage Examples

## Get Media Info

```python
media_info = await pnp.get_media_info()
print(media_info.artist, media_info.title)
```

## Control Playback

```python
await pnp.play()
await pnp.pause()
await pnp.next_track()
await pnp.seek(60)  # Seek to 1 minute
```

## Get Timeline Properties

```python
timeline = await pnp.get_timeline_properties()
print(timeline.position, timeline.end_time)
```

## Register for Playback Info Changes

```python
def on_playback_info_changed(info):
    print("Playback status changed:", info.playback_status)

pnp.register_playback_info_changed_callback(on_playback_info_changed)
```

# Dataclasses

All returned objects are typed dataclasses for easy access and type safety:

- `MediaInfo`: artist, title, album, genres, thumbnail, etc.
- `PlaybackInfo`: playback status, type, rate, repeat/shuffle state, controls.
- `MediaTimeline`: position, start/end time, seek times.
- `EnabledControls`: which playback controls are available for the current app.

# Advanced: Discord RPC Example

See `examples/discordRPC_v4.pyw` for a full Discord Rich Presence integration using Py Now Playing.

# Troubleshooting

- Ensure a media app is open and playing media for most features to work.
- Windows only: This library uses WinRT APIs and only works on Windows 10/11.
- Asyncio required: All API calls are async; use `await` and run your code in an async event loop.

# Contributing

Pull requests, issues, and feature suggestions are welcome!  
See the code for docstrings and usage examples.