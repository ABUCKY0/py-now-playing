import sys
sys.path.append('.')
sys.path.append('..')
import py_now_playing
import asyncio
from pypresence import Presence
import pypresence.exceptions
from pypresence.exceptions import InvalidID
import time
import multiprocessing
import logging
import os
import sys
import traceback
import re
import requests
# Set up logging
#logging.basicConfig(level=logging.NOTSET)
logging.basicConfig(level=logging.INFO)
# Set up logging to a file
logging.basicConfig(filename='C:/Users/buckn/OneDrive/Documents/py-now-playing/tests/app.log', level=logging.INFO)

# Disable logging to consile with sys
#sys.stdout = open(os.devnull, 'w')
#sys.stderr = open(os.devnull, 'w')
#logging = logging.getlogging(__name__)


def get_album_art(artist, title):
    # adapted from https://github.com/NextFire/apple-music-discord-rpc/blob/main/music-rpc.ts#L186
    # Uses https://musicbrainz.org/
    # Uses https://coverartarchive.org/
    def lucene_escape(term):
        return re.sub(r'([+\-&|!(){}\[\]^"~*?:\\])', r'\\\1', term)

    def remove_parentheses_content(term):
        return re.sub(r'\([^)]*\)', '', term).strip()
    query_terms = []
    MB_EXCLUDED_NAMES = ['Various Artists', 'Various', 'Unknown Artist', 'Unknown']
    if not all(elem in artist for elem in MB_EXCLUDED_NAMES):
        query_terms.append(f'artist:"{lucene_escape(remove_parentheses_content(artist))}"')
    if title is not None:
        query_terms.append(f'recording:"{lucene_escape(remove_parentheses_content(title))}"')
    query = " ".join(query_terms)

    params = {
        'fmt': 'json',
        'limit': '10',
        'query': query,
    }

    resp = requests.get('https://musicbrainz.org/ws/2/release', params=params)
    json = resp.json()

    for release in json['releases']:
        resp = requests.get(f'https://coverartarchive.org/release/{release["id"]}/front')
        if resp.status_code == 200:
            print(resp.url)
            return resp.url
    return None

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

    while True:
        try:
            now_playing_list = now_playing_queue.get()
            logging.info(now_playing_list)
            if now_playing_list:
                print("retrieved now_playing_list" + str(now_playing_list))
                rpc.update(
                    details=now_playing_list['title'] or "Unknown Song", 
                    state='by ' + now_playing_list['artist'] if now_playing_list['artist'] is not None else 'by Unknown Artist',
                    large_image=get_album_art(now_playing_list['artist'],now_playing_list['title']),  # Replace with your image key
                    large_text='Amazon Music',
                )
            else:
                logging.info("No Music Playing")
                rpc.clear()
        except (pypresence.exceptions.DiscordNotFound, pypresence.exceptions.InvalidPipe, pypresence.PipeClosed) as e:
            connect_rpc()
        except BrokenPipeError or EOFError as f:
            logging.error(f"BrokenPipeError: {f}")
            traceback.print_exc()
        except EOFError or UnboundLocalError as g:
            logging.error(f"EOFError: {g}")
            traceback.print_exc()

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

    try:
        while True:
            now_playing = await np.get_active_app_user_model_ids()
            print (now_playing)
            #now_playing = list(filter(lambda app: app['Name'] == 'Amazon Music', now_playing))
            # AppID Specifically I'm looking for is Chrome._crx_mnlencgjbmniianjkpemfocoke
            now_playing = list(filter(lambda app: app['AppID'] == 'Chrome._crx_mnlencgjbmniianjkpemfocoke', now_playing))
            if not now_playing:
                now_playing_queue.put(None)
                await asyncio.sleep(5)
                continue

            now_playing_appid = now_playing[0]['AppID']
            try:
                data = await np.get_now_playing(now_playing_appid)
                # if 'thumbnail' in data:
                #     del data['thumbnail']
                
                # Turn thumbnail into a photo using async def thumbnail_to_image(self, thumbnail):
                if 'thumbnail' in data:
                    data['thumbnail'] = await np.thumbnail_to_image(data['thumbnail'])
                
            except PermissionError as permerr:
                # logging.error("PermissionError: ")
                # traceback.print_exc()
                # data = None
                pass
            now_playing_queue.put(data)
            logging.info("A Song is Playing, Here is the Json for that: " + str(data))
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        logging.info("Interrupted by user, stopping processes...")
        rpc_process.terminate()  # Terminate the rpc_process
        # Kill the event loop
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