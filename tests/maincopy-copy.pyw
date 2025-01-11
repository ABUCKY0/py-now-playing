import sys
sys.path.append('C:/Users/buckn/Documents/py-now-playing')
import py_now_playing
import asyncio
from pypresence import Presence
import pypresence.exceptions
from pypresence.exceptions import InvalidID
import time
import multiprocessing
import logging
import os
import traceback
import re
import requests
import SECRETS
from datetime import datetime, timedelta
from urllib.parse import quote
# Set up logging
logging.basicConfig(filename='C:/Users/buckn/Documents/py-now-playing/tests/app.log', level=logging.DEBUG)

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
        token_expiration = datetime.now() + timedelta(seconds=auth_response_data['expires_in'])
    
    return spotify_token

def get_album_art(artist, title):
    token = get_spotify_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    query = f'artist:{artist} track:{title}'
    print(query)
    print(quote(query))
    response = requests.get(f'https://api.spotify.com/v1/search?q={quote(query)}&type=track&limit=1', headers=headers)
    response_data = response.json()
    print(response_data)
    
    if response_data['tracks']['items']:
        album_art_url = response_data['tracks']['items'][0]['album']['images'][0]['url']
        return album_art_url
    else:
        logging.error("Failed to get album art: No items found")
        return "https://pro2-bar-s3-cdn-cf4.myportfolio.com/42020405547ae2dc93d34e8df7965fc4/5d5b55e2-c1b4-46cb-a027-6a21bee9de3f_rw_1920.gif?h=85babbd0e5d4aa7c618295a359c1811f"

def start_rpc(client_id, now_playing_queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    rpc = Presence(client_id)

    def connect_rpc():
        while True:
            try:
                logging.info("try to connect")
                rpc.connect()
                logging.info("Connected to Discord RPC")
                break
            except Exception as e:
                logging.error(f"Failed to connect to Discord RPC: {e}")
                traceback.print_exc()
                time.sleep(15)

    # Call connect_rpc directly
    connect_rpc()

    current_song = None

    while True:
        try:
            now_playing_list = now_playing_queue.get()
            if now_playing_list:
                new_song = (now_playing_list['artist'], now_playing_list['title'])
                if new_song != current_song:
                    current_song = new_song
                    rpc.update(
                        details=now_playing_list['title'] or "Unknown Song", 
                        state='by ' + now_playing_list['artist'] if now_playing_list['artist'] is not None else 'by Unknown Artist',
                        large_image=get_album_art(now_playing_list['artist'], now_playing_list['title']),  # Replace with your image key
                        small_image="https://i.pinimg.com/736x/de/16/6c/de166cc1fbe405eb8f7725145f9a488a.jpg",
                        small_text='Powered by py-now-playing, on Amazon Music')
                rpc.clear()
        except (pypresence.exceptions.DiscordNotFound, pypresence.exceptions.InvalidPipe, pypresence.PipeClosed) as e:
            connect_rpc()
        except BrokenPipeError or EOFError as f:
            logging.error(f"BrokenPipeError: {f}")
            traceback.print_exc()
        except EOFError or UnboundLocalError as g:
            logging.error(f"EOFError: {g}")
            traceback.print_exc()
        except Exception as e:
            logging.error(f"Unexpected error in start_rpc: {e}")
            traceback.print_exc()
            pass

        time.sleep(5)

async def main():
    np = py_now_playing.NowPlaying()
    await np.initalize_mediamanger()

    client_id = '1187213553673965619'  # Replace with your client ID
    manager = multiprocessing.Manager()
    now_playing_queue = manager.Queue()

    # Start the Discord RPC in a separate process
    rpc_process = multiprocessing.Process(target=start_rpc, args=(client_id, now_playing_queue))
    rpc_process.start()

    current_song = None

    try:
        while True:
            now_playing = await np.get_active_app_user_model_ids()
            now_playing = list(filter(lambda app: app['AppID'] == 'ChromeDev._crx_hjlgoickghknhfichlenalencg', now_playing))
            if not now_playing:
                while not now_playing_queue.empty():
                    now_playing_queue.get()

                now_playing_queue.put(None)
                await asyncio.sleep(5)
                continue

            now_playing_appid = now_playing[0]['AppID']
            try:
                data = await np.get_now_playing(now_playing_appid)
                if 'thumbnail' in data:
                    data['thumbnail'] = await np.thumbnail_to_image(data['thumbnail'])
                    
            except PermissionError as permerr:
                logging.error("PermissionError: ")
                traceback.print_exc()
                data = None
                pass
            while not now_playing_queue.empty():
                now_playing_queue.get()

            new_song = (data['artist'], data['title'])
            if new_song != current_song:
                current_song = new_song
                now_playing_queue.put(data)
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        logging.info("Interrupted by user, stopping processes...")
        rpc_process.terminate()  # Terminate the rpc_process
        asyncio.get_event_loop().stop()
    except OSError as e:
        logging.error(f"OSError {e}")
        traceback.print_exc()
        now_playing_queue.put(None)
    except Exception as e:
        logging.error(f"Unexpected error in main: {e}")
        traceback.print_exc()
        pass

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Interrupted by user, caught in if, exiting...")
        sys.exit(0)