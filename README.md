# Py Now Playing

Py Now Playing lets you read and control media sessions from Windows apps via the Global System Media Transport Controls (GSMTC) API.

Originally, this began as a personal project to feed the currently playing audio from a specific app into a Discord Rich Presence. The Windows APIs for this aren’t the friendliest, so I built a Python interface around them.

> **Note:** This library is **Windows-only** and uses `asyncio`. Most functions must be awaited.

---

## Importing

You can import everything with:

```python
from py_now_playing import *
```

Or, for clarity, import only what you need:

```python
from py_now_playing import PyNowPlaying, MediaInfo, PlaybackInfo
```

---

## Setup

Initializing a `PyNowPlaying` instance requires the **AppUserModelID (AUMID)** of the target app.

Static helpers are provided:

```python
# Get currently playing apps and their IDs
ids = await PyNowPlaying.get_active_app_user_model_ids()
# -> [{"Name": "Spotify", "AppID": "Spotify_AUMID"}, ...]

# Find all apps matching a name
matches = await PyNowPlaying.get_all_aumids_by_name("Spotify")
```

> Alternatively, in PowerShell:
>
> ```powershell
> Get-StartApps | Select-String "App Name"
> ```

---

## Initialization

```python
pnp = await PyNowPlaying.create(aumid="Spotify_AUMID")
```

---

## Usage Examples

### Get Media Info

```python
media_info = await pnp.get_media_info()
print(media_info.artist, media_info.title)
```

### Control Playback

```python
await pnp.play()
await pnp.pause()
await pnp.next_track()
await pnp.seek(60)  # Seek to 1 minute
```

### Get Timeline Properties

```python
timeline = await pnp.get_timeline_properties()
print(timeline.position, timeline.end_time)
```

### Register for Playback Info Changes

```python
def on_playback_info_changed(info):
    print("Playback status changed:", info.playback_status)

pnp.register_playback_info_changed_callback(on_playback_info_changed)
```

---

## Dataclasses

All returned objects are typed dataclasses:

- **`MediaInfo`** – Artist, title, album, genres, thumbnail, etc.
- **`PlaybackInfo`** – Playback status, type, rate, repeat/shuffle state, controls.
- **`MediaTimeline`** – Position, start/end time, seek times.
- **`EnabledControls`** – Which controls are available for the current app.

---

## Advanced Example: Discord RPC

See [`examples/discordRPC_v4.pyw`](examples/discordRPC_v4.pyw) for a full Discord Rich Presence integration.

See [`examples/controlpanel.py`](examples/controlpanel.py) for a basic control panel written with Flet.
---

## Troubleshooting

- Ensure the target media app is open and actively playing.
- Works only on Windows 10/11 (uses WinRT APIs).
- All calls are **async**; use `await` inside an async event loop.

---

## Contributing

Pull requests, issues, and feature suggestions are welcome.  
Check the code for docstrings and usage examples.
