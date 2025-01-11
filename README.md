# Py Now Playing

This project started as me wanting to create a Discord RPC that would take the currently playing audio from a specified application, and put that onto my Discord activity. I found some windows apis that allow me to do this, however they weren't intuitive to use. So, I started this. 

Note that this class utilizes asyncio, so you may need to use await when using this class.
# How to use

```py
# Initalize the Class
np = NowPlaying()

#initalize the mediamanager
await np.initalize_mediamanager()
```

To get the active media apps, use `get_active_app_user_model_ids()`.
Then you can use a filter or a loop to find the application you're looking for.
`list(filter(lambda app: app['Name'] == 'App Name', now_playing))`

Then use something like `now_playing[0]['AppID']` to get the appid from the filter, and pass that into `get_now_playing(app_user_model_id)` to get the currently playing media for that application.
 
## Other Notes


I've noticed that even when using Firefox and watching YouTube videos, that the playback_type is still MediaPlaybackType.MUSIC. I'll have to figure out why and if that changes at all.


Note that if you're testing the Amazon Music RPC I made in /tests, because Amazon has a skill issue Amazon Music doesn't always report the current song to Windows properly, so it may not appear correct.


![image](https://github.com/user-attachments/assets/53b3bb1e-6c31-4385-970b-ba66384eec0d)  
Above: An Amazon Music Discord RPC Application using Py Now Playing and Pypresence. Note that the album covers aren't the ones pulled from Windows, and are instead pulled from the Spotify API.
