# Py Now Playing

This project started as me wanting to create a Discord RPC that would take the currently playing audio from a specified application, and put that onto my Discord activity. I found some windows apis that allow me to do this, however they weren't intuitive to use. So, I started this. 

Note that this class utilizes asyncio, so you may need to use await when using this class.

# Importing
You can use the following import statement to import all parts of py_now_playing
```py
from py_now_playing import MediaPlaybackStatus, MediaPlaybackType, MediaPlaybackAutoRepeatMode, PlaybackInfo, MediaTimeline, PlaybackControls, MediaInfo
```


# Py Now Playing in Use
![image](https://github.com/user-attachments/assets/53b3bb1e-6c31-4385-970b-ba66384eec0d)  
Above: An Amazon Music Discord RPC Application using Py Now Playing and Pypresence. Note that the album covers aren't the ones pulled from Windows, and are instead pulled from the Spotify API.
