# Py Now Playing

This project started as me wanting to create a Discord RPC that would take the currently playing audio from a specified application, and put that onto my Discord activity. I found some windows apis that allow me to do this, however they weren't intuitive to use. So, I started this. 


# How to use

Instantiate the Class using `py_now_playing.create()`. You ***MUST*** use the create method. You can however use the create method as if you instantiated just the class. 

Then, you can use the different methods I haven't documented that aren't preflixed with an _ in py_now_playing/\_\_init\_\_.py

If you're running an audio application, but you don't know what the AppID is, (App IDs are how the Windows SDK refers to apps), run `get_active_app_audio_model_ids()` to get a list of all applications that are currently playing audio, with their name and their app id.

Then taking that AppID from above, you can pass it into `get_now_playing()`, which will return the currently playing audio for that application. 

If you want the thumbnail, take the thumbnail portion of the above method, and pass that into `thumbnail_to_image()`, which will return a PIL (Pillow) Image.
 
## Other Notes


I've noticed that even when using Firefox and watching YouTube videos, that the playback_type is still MediaPlaybackType.MUSIC. I'll have to figure out why and if that changes at all.


Note that if you're testing the Amazon Music RPC I made in /tests, because Amazon has a skill issue Amazon Music doesn't always report the current song to Windows properly, so it may not appear correct.


![image](https://github.com/ABUCKY0/py-now-playing/assets/81783950/ad175e42-8fbe-4a64-824c-f1c6ef173bbb)
