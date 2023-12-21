# Py Now Playing

This project started as me wanting to create a Discord RPC that would take the currently playing audio from a specified application, and put that onto my Discord activity. I found some windows apis that allow me to do this, however they weren't intuitive to use. So, I started this. 


# How to use

Instantiate the Class using `py_now_playing.create()`. You ***MUST*** use the create method. You can however use the create method as if you instantiated just the class. 

Then, you can use the different methods I haven't documented that aren't preflixed with an _ in py_now_playing/\_\_init\_\_.py

### Output
```text
{'album_artist': '', 'album_title': '', 'album_track_count': 0, 'artist': 'The Killers', 'genres': [], 'playback_type': <MediaPlaybackType.MUSIC: 1>, 'subtitle': '', 'thumbnail': None, 'title': 'Your Side of Town', 'track_number': 0}
```


## Other Notes


I've noticed that even when using Firefox and watching YouTube videos, that the playback_type is still MediaPlaybackType.MUSIC. I'll have to figure out why and if that changes at all.