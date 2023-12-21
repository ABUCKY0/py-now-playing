# Py Now Playing

This project started as me wanting to create a Discord RPC that would take the currently playing audio from a specified application, and put that onto my Discord activity. I found some windows apis that allow me to do this, however they weren't intuitive to use. So, I started this. 

# Roadmap

1) Make getting album images easier
2) Other things I can't think of.

# How to use

***This is coming soon, however i've provided some simple test code I made that prints the json output from the library.***

```python3
import sys
sys.path.append('.')
import py_now_playing
import asyncio
import json

async def main():
    np = await py_now_playing.NowPlaying.create()
    now_playing = await np.get_active_app_audio_model_ids()
    now_playing = [app for app in now_playing if app['Name'] == 'Amazon Music']
    now_playing_appid = now_playing[0]['AppID']
    now_playing = await np.get_now_playing(now_playing_appid)
    print(now_playing)

if __name__ == '__main__':
    asyncio.run(main())
```

### Output
```text
{'album_artist': '', 'album_title': '', 'album_track_count': 0, 'artist': 'The Killers', 'genres': [], 'playback_type': <MediaPlaybackType.MUSIC: 1>, 'subtitle': '', 'thumbnail': None, 'title': 'Your Side of Town', 'track_number': 0}
```


## Other Notes


I've noticed that even when using Firefox and watching YouTube videos, that the playback_type is still MediaPlaybackType.MUSIC. I'll have to figure out why and if that changes at all.