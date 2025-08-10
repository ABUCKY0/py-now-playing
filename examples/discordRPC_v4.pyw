import sys
import re
import asyncio
import logging
import requests
from datetime import datetime, timedelta
from urllib.parse import quote
from pypresence import AioPresence, ActivityType, exceptions as rpc_exceptions

import SECRETS

sys.path.extend([
    'C:/Users/buckn/Documents/py-now-playing',
    'C:/Users/buckn/Documents/py-now-playing/py_now_playing'
])

from py_now_playing import (
    PyNowPlaying, MediaPlaybackStatus
)
# --- Logging Setup ---
logging.basicConfig(
    filename='C:/Users/buckn/Documents/py-now-playing/examples/app3.log',
    level=logging.DEBUG,
    format="(%(filename)s:%(lineno)d) [%(levelname)s] - %(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)
# \***** Console Logger *****
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(console)

# set logging level of PngImagePlugin.py (PIL)
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

# --- Constants ---
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_SEARCH_URL = 'https://api.spotify.com/v1/search'
DEFAULT_IMAGE = "https://pro2-bar-s3-cdn-cf4.myportfolio.com/42020405547ae2dc93d34e8df7965fc4/5d5b55e2-c1b4-46cb-a027-6a21bee9de3f_rw_1920.gif?h=85babbd0e5d4aa7c618295a359c1811f"
PLAY_ICON = "https://thumbs.dreamstime.com/b/white-play-button-middle-black-square-white-play-button-middle-black-square-291113889.jpg"
PAUSE_ICON = "https://static-00.iconduck.com/assets.00/pause-button-icon-512x512-uec65jbo.png"

# --- Spotify Token Handling ---
SPOTIFY_TOKEN = None
TOKEN_EXPIRATION = None


def get_spotify_token():
    """Fetches a new Spotify token if the current one is expired or not set."""
    global SPOTIFY_TOKEN, TOKEN_EXPIRATION
    if not SPOTIFY_TOKEN or datetime.now() >= TOKEN_EXPIRATION:
        try:
            response = requests.post(SPOTIFY_AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': SECRETS.CLIENT_ID,
                'client_secret': SECRETS.CLIENT_SECRET,
            }, timeout=30)
            response_data = response.json()
            SPOTIFY_TOKEN = response_data['access_token']
            TOKEN_EXPIRATION = datetime.now(
            ) + timedelta(seconds=response_data['expires_in'])
        except Exception as e:
            logger.exception("Failed to get Spotify token: %s", e)
            return None
    return SPOTIFY_TOKEN


def get_album_art(artist, title):
    """Fetches album art from Spotify based on artist and title."""
    token = get_spotify_token()
    if not token:
        return DEFAULT_IMAGE

    query = quote(f'artist:{artist} track:{title}')
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(
            f'{SPOTIFY_SEARCH_URL}?q={query}&type=track&limit=1', headers=headers, timeout=30)
        items = response.json().get('tracks', {}).get('items', [])
        return items[0]['album']['images'][0]['url'] if items else DEFAULT_IMAGE
    except Exception as e:
        logger.exception("Error retrieving album art: %s", e)
        return DEFAULT_IMAGE

# --- Main Async Function ---


async def main():
    """Main function to initialize the playback controls and Discord RPC."""
    # np = PlaybackControls(aumid="ChromeDev._crx_hjlgoickghknhfichlenalencg")
    np = PyNowPlaying(aumid="music.amazon.com-6BE721EE_pwn81ww419gp8!App")
    await np.initalize_mediamanager()

    rpc = AioPresence("1187213553673965619")
    while True:
        try:
            await rpc.connect()
            logger.info("Connected to Discord RPC")
            break
        except (rpc_exceptions.DiscordNotFound, rpc_exceptions.InvalidID) as e:
            logger.exception("Discord RPC connection failed: %s", e)
            await asyncio.sleep(5)
        except Exception as e:
            logger.exception(
                "Error in main during first RPC Connect %s", str(e))

    prev_state = {}
    was_cleared = False
    while True:
        try:
            media_info = await np.get_media_info()
            media_timeline = await np.get_timeline_properties()
            media_playback = await np.get_playback_info()

            if not (media_info and media_info.title and media_info.artist and media_playback) and not was_cleared:
                await rpc.clear()
                logger.debug("Cleared Discord RPC")
                prev_state.clear()
                was_cleared = True

                await asyncio.sleep(1)
                continue
            elif not (media_info and media_info.title and media_info.artist and media_playback):
                await asyncio.sleep(1)
                continue

            state_changed = (
                media_info.title != prev_state.get('title') or
                media_info.artist != prev_state.get('artist') or
                media_playback.playback_status != prev_state.get('status')
            )

            if state_changed:
                logger.info("Media state changed. Updating Discord RPC.")
                was_cleared = False
                title = re.sub(r"\[.*?feat\..*?\]", "", media_info.title).removesuffix(
                    " [Explicit]").removesuffix(" [Clean]").strip()
                artists = re.findall(r'\[.*?feat\.(.*?)\]', media_info.title)
                artist_names = [media_info.artist] + [a.strip()
                                                      for feat in artists for a in feat.split('&')]
                artist = ', '.join([re.sub(r'\[.*?\]', '', a).strip()
                                   for a in artist_names])

                album_art_url = get_album_art(artist, title)
                mini_icon = PLAY_ICON if media_playback.playback_status == MediaPlaybackStatus.PLAYING else PAUSE_ICON

                start_time = int(datetime.now().timestamp() -
                                 media_timeline.position.seconds)
                end_time = int(start_time + media_timeline.end_time.seconds)

                await rpc.update(
                    state=f"by {artist}",
                    details=title,
                    large_image=album_art_url,
                    small_image=mini_icon,
                    small_text="Playing" if media_playback.playback_status == MediaPlaybackStatus.PLAYING else "Paused",
                    large_text="Listening on Amazon Music",
                    activity_type=ActivityType.LISTENING,
                    start=start_time,
                    end=end_time,
                    name=f"{artist}",
                )

                prev_state.update({
                    'title': media_info.title,
                    'artist': media_info.artist,
                    'status': media_playback.playback_status
                })

            await asyncio.sleep(1)

        except (rpc_exceptions.DiscordNotFound, rpc_exceptions.InvalidPipe, rpc_exceptions.PipeClosed, rpc_exceptions.DiscordError, rpc_exceptions.ConnectionTimeout):
            while True:
              try:
                  await rpc.connect()
                  logger.info("Connected to Discord RPC")
                  break
              except (rpc_exceptions.DiscordNotFound, rpc_exceptions.InvalidID) as e:
                  logger.exception("Discord RPC connection failed: %s", e)
                  await asyncio.sleep(5)
        except Exception as e:
            logger.exception("Unexpected error: %s", e)
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
