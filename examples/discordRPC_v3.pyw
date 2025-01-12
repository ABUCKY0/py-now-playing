from urllib.parse import quote
from datetime import datetime, timedelta
import SECRETS
import requests
import re
import traceback
import os
import logging
import multiprocessing
import time
from pypresence import ActivityType
from pypresence.exceptions import InvalidID
import pypresence.exceptions
from pypresence import Presence
import asyncio
from py_now_playing import PlaybackControls, PlaybackInfo, MediaInfo, MediaTimeline
import sys
from dataclasses import dataclass
sys.path.append('C:/Users/buckn/Documents/py-now-playing')

# install dev build of pypresence = pip install https://github.com/qwertyquerty/pypresence/archive/f856ccaaeb2321f64f9692b75dc3ceda5c927f42.zip
# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='(%(filename)s:%(lineno)d) - %(asctime)s - %(message)s')
logging.basicConfig(
    filename='C:/Users/buckn/Documents/py-now-playing/examples/app.log', level=logging.DEBUG, format="(%(filename)s:%(lineno)d) - %(asctime)s - %(message)s")
# console debug logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# filter PIL Image
logging.getLogger('PIL').setLevel(logging.INFO)
spotify_token = None
token_expiration = None


def get_spotify_token():
  global spotify_token, token_expiration
  if spotify_token is None or datetime.now() >= token_expiration:
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': SECRETS.CLIENT_ID,
        'client_secret': SECRETS.CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    spotify_token = auth_response_data['access_token']
    token_expiration = datetime.now(
    ) + timedelta(seconds=auth_response_data['expires_in'])

  return spotify_token


def get_album_art(artist, title):
  token = get_spotify_token()
  headers = {
      'Authorization': f'Bearer {token}'
  }
  query = f'artist:{artist} track:{title}'
  logger.debug("Query Being Sent to Spotify: " + query)
  logger.debug("Query Being Sent to Spotify (URL Encoded): " + quote(query))
  response = requests.get(
      f'https://api.spotify.com/v1/search?q={quote(query)}&type=track&limit=1', headers=headers)
  response_data = response.json()
  logger.debug("Response from Spotify: " + str(response_data))

  if response_data['tracks']['items']:
    album_art_url = response_data['tracks']['items'][0]['album']['images'][0]['url']
    return album_art_url
  else:
    logger.error("Failed to get album art: No items found")
    return "https://pro2-bar-s3-cdn-cf4.myportfolio.com/42020405547ae2dc93d34e8df7965fc4/5d5b55e2-c1b4-46cb-a027-6a21bee9de3f_rw_1920.gif?h=85babbd0e5d4aa7c618295a359c1811f"


def start_rpc(client_id, now_playing_queue):
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

  rpc = Presence(client_id)

  def connect_rpc():
    while True:
      try:
        logger.debug("Attempting to Connect to Discord RPC")
        rpc.connect()
        logger.debug("Connected to Discord RPC")
        break
      except Exception as e:
        logger.error(f"Failed to connect to Discord RPC: {e}")
        traceback.print_exc()
        time.sleep(15)

  # Call connect_rpc directly
  connect_rpc()

  current_song = None

  while True:
    try:
      now_playing_song: Objects = now_playing_queue.get()
      if now_playing_song:
        # Playing and paused status
        # logger.log(logging.DEBUG, f"Playback Status: {now_playing_song.PlaybackInfo.playback_status}")
        if now_playing_song.MediaInfo.title != (current_song.MediaInfo.title if current_song is not None else None):
          logger.debug(f"New Song: {now_playing_song.MediaInfo.title}")
          current_song = now_playing_song
          logger.debug(f"Current Song: {current_song.MediaInfo.title}")
          rpc.update(
              activity_type=ActivityType.LISTENING,
              details=now_playing_song.MediaInfo.title or "Unknown Song",
              state='by ' +
              now_playing_song.MediaInfo.artist if now_playing_song.MediaInfo.artist is not None else 'by Unknown Artist',
              # Replace with your image key
              large_image=get_album_art(
                  now_playing_song.MediaInfo.artist, now_playing_song.MediaInfo.title.removesuffix(" [Explicit]")),
              small_image="https://i.pinimg.com/736x/de/16/6c/de166cc1fbe405eb8f7725145f9a488a.jpg",
              small_text='Powered by py-now-playing, on Amazon Music',
              buttons=[{"label": "Powered by py-now-playing",
                        "url": "https://github.com/abucky0/py-now-playing"}]
          )
      else:
        rpc.clear()
        current_song = None
    except (pypresence.exceptions.DiscordNotFound, pypresence.exceptions.InvalidPipe, pypresence.PipeClosed) as e:
      connect_rpc()
    except (BrokenPipeError, EOFError) as f:
      logger.error(f"BrokenPipeError: {f}")
      traceback.print_exc()
    except (EOFError, UnboundLocalError) as g:
      logger.error(f"EOFError: {g}")
      traceback.print_exc()
    except Exception as e:
      logger.error(f"Unexpected error in start_rpc: {e}")
      traceback.print_exc()

    time.sleep(.1)


@dataclass
class Objects:
  MediaTimeline: MediaTimeline
  PlaybackInfo: PlaybackInfo
  MediaInfo: MediaInfo


async def main():
  np = PlaybackControls(aumid="ChromeDev._crx_hjlgoickghknhfichlenalencg")
  await np.initalize_mediamanager()

  client_id = '1187213553673965619'  # Replace with your client ID
  manager = multiprocessing.Manager()
  now_playing_queue = manager.Queue()

  # Start the Discord RPC in a separate process
  rpc_process = multiprocessing.Process(
      target=start_rpc, args=(client_id, now_playing_queue))
  rpc_process.start()

  current_song = None
  try:
    while True:
      # now_playing = await np.get_active_app_user_model_ids()
      # now_playing = list(filter(
      #     lambda app: app['AppID'] == 'ChromeDev._crx_hjlgoickghknhfichlenalencg', now_playing))
      # if not now_playing:
      #   while not now_playing_queue.empty():
      #     now_playing_queue.get()

      #   now_playing_queue.put(None)
      #   await asyncio.sleep(5)
      #   continue

      # now_playing_appid = now_playing[0]['AppID']
      # try:
      #   data = await np.get_now_playing(now_playing_appid)
      #   if 'thumbnail' in data:
      #     data['thumbnail'] = await np.thumbnail_to_image(data['thumbnail'])

      # except PermissionError as permerr:
      #   logger.error("PermissionError: ")
      #   traceback.print_exc()
      #   data = None
      #   pass
      # while not now_playing_queue.empty():
      #   now_playing_queue.get()

      if await np.get_timeline_properties() is None or await np.get_playback_info() is None or await np.get_media_info() is None:
        now_playing_queue.put(None)
      else:
        data = Objects(await np.get_timeline_properties(), await np.get_playback_info(), await np.get_media_info())
        now_playing_queue.put(data)
      await asyncio.sleep(1)
  except KeyboardInterrupt:
    logger.info("Interrupted by user, stopping processes...")
    rpc_process.terminate()  # Terminate the rpc_process
    asyncio.get_event_loop().stop()
  except OSError as e:
    logger.error(f"OSError {e}")
    traceback.print_exc()
    now_playing_queue.put(None)
  except Exception as e:
    logger.error(f"Unexpected error in main: {e}")
    traceback.print_exc()
    pass


if __name__ == '__main__':
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    logger.error("KeyboardInterrupt-ed by user, caught in if, exiting...")
    sys.exit(0)
  except Exception as e:
    logger.error(f"Unexpected error in __main__: {e}")
    traceback.print_exc()
    sys.exit(1)
