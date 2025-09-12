# Py Now Playing ![PyPI](https://img.shields.io/pypi/v/py-now-playing) ![License](https://img.shields.io/badge/license-GPLv3-brightgreen)  
Py Now Playing lets you read and control media sessions from Windows apps via the Global System Media Transport Controls (GSMTC) API.  

### Features

- Fetch track details (artist, title, album, artwork)  
- Control playback (play, pause, seek, next/previous)  
- Access timeline info (position, duration)  
- Register callbacks for status changes  

Originally developed to feed currently playing audio into Discord Rich Presence, Py Now Playing provides an easy Python interface for controlling media apps on Windows.

> **Note:** Windows-only. Uses `asyncio`; all functions are asynchronous and must be awaited.

---

## Installation

```bash
pip install py-now-playing
```

---

## Importing

You can import everything:

```python
from py_now_playing import *
```

Or selectively import only what you need:

```python
from py_now_playing import (
    MediaPlaybackStatus,
    MediaPlaybackType,
    MediaPlaybackAutoRepeatMode,
    PlaybackInfo,
    MediaTimeline,
    PyNowPlaying,
    MediaInfo
)
```

---

## Finding App User Model IDs (AUMID)

Every Windows media app has a unique App User Model ID (AUMID). Py Now Playing uses this ID to connect and control the app.

### Using Static Functions

```python
# Get currently active media apps and their IDs
ids = await PyNowPlaying.get_active_app_user_model_ids()
# -> [{"Name": "Spotify", "AppID": "Spotify_AUMID"}, ...]

# Find all apps matching a name
matches = await PyNowPlaying.get_all_aumids_by_name("Spotify")
```

### Command Line / PowerShell

- Run Py Now Playing from the command line to list apps:

```bash
python -m py-now-playing
```

- Or in PowerShell:

```powershell
Get-StartApps | Select-String "App Name"
```

---

## Quick Start

```python
import asyncio
from py_now_playing import PyNowPlaying

async def main():
    pnp = await PyNowPlaying.create(aumid="Spotify_AUMID")
    media = await pnp.get_media_info()
    print(media.artist, media.title)

asyncio.run(main())
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

### Access Timeline Properties

```python
timeline = await pnp.get_timeline_properties()
# timeline contains position, start/end time, and seek times (see MediaTimeline dataclass)
print(timeline.position, timeline.end_time)
```

### Register a Playback Callback

```python
def on_playback_info_changed(info):
    print("Playback status changed:", info.playback_status)

pnp.register_playback_info_changed_callback(on_playback_info_changed)
```

---

## Dataclasses Overview

| Class | Description |
|-------|-------------|
| **MediaInfo** | Artist, title, album, genres, artwork, etc. |
| **PlaybackInfo** | Playback status, type, rate, repeat/shuffle state, available controls |
| **MediaTimeline** | Position, start/end time, seek times |
| **EnabledControls** | Which controls are available for the current app |

---

## Advanced Example: Discord RPC
> [!NOTE]
> None of these examples are guaranteed to work on your system because I hardcoded file paths for logs and paths. They are shown as examples *only*.
- [\`examples/discordRPC_v4.pyw\`](examples/discordRPC_v4.pyw) – full Discord Rich Presence integration  
- [\`examples/controlpanel.py\`](examples/controlpanel.py) – basic control panel using Flet  

---

## Troubleshooting

- Ensure the target media app is open and actively playing.  
- Works only on Windows 10/11 (uses WinRT APIs).  
- All calls are async; use `await` inside an async event loop.  
- If no media info is returned, verify that the app is playing media and the AUMID is correct.  

---

## License

This project is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file for details.
