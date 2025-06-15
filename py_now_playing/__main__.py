# from py_now_playing.media_timeline import MediaTimeline
# from py_now_playing.playback_info import PlaybackInfo, MediaPlaybackStatus, MediaPlaybackType, MediaPlaybackAutoRepeatMode
from py_now_playing.pnp import PyNowPlaying
# from py_now_playing.media_info import MediaInfo
import asyncio
import argparse

async def run_cli():
  parser = argparse.ArgumentParser(description="Run the Now Playing application.")
  media_apps = await PyNowPlaying.get_active_app_user_model_ids()
  for app in media_apps:
    print(f"{app['Name']} ({app['AppID']})")
    pnp = PyNowPlaying(aumid=app['AppID'])
    await pnp.initalize_mediamanager()
    media_name = await pnp.get_media_info()
    if media_name:
      print(f"Currently Playing: \"{media_name.title}\" by \"{media_name.artist}\"")
    else:
      print("No media is currently playing.")
    print("\n--------------------------------\n")

if __name__ == "__main__":
  asyncio.run(run_cli())
